from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product
from sentence_transformers import SentenceTransformer, util
from transformers import T5Tokenizer, T5ForConditionalGeneration
from app.schemas.recommend import RecommendRequest  # Import the schema

# Load the SentenceTransformer model for embeddings
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Load the T5 model and tokenizer for text generation
tokenizer = T5Tokenizer.from_pretrained("t5-small")
t5_model = T5ForConditionalGeneration.from_pretrained("t5-small")


# Retrieve top products based on semantic similarity
async def retrieve_top_products(query: str, db: AsyncSession, limit: int = 3) -> dict:
    """
    Retrieve the top products based on semantic similarity to the query.

    Args:
        query (str): The user's search query.
        db (AsyncSession): The database session for querying products.
        limit (int): The maximum number of top products to retrieve.

    Returns:
        dict: A dictionary containing the top products, the closest match,
              and fallback suggestions if no good matches are found.
    """
    # Query all products from the database
    result = await db.execute(select(Product))
    products = result.scalars().all()

    # Handle the case where no products are available
    if not products:
        return {
            "products": [],
            "closest_item": None,
            "fallback_suggestions": ["Check back later – our catalog might be growing!"]
        }

    # Generate embeddings for the query and product descriptions
    descriptions = [p.description or p.name for p in products]
    query_embedding = embedding_model.encode(query, convert_to_tensor=True)
    product_embeddings = embedding_model.encode(descriptions, convert_to_tensor=True)

    # Compute cosine similarity between the query and product embeddings
    similarities = util.pytorch_cos_sim(query_embedding, product_embeddings)[0]
    top_indices = similarities.argsort(descending=True)[:limit]  # Get indices of top matches

    # Retrieve the top products and their similarity scores
    top_products = [products[i.item()] for i in top_indices]
    closest_score = similarities[top_indices[0]].item()
    closest_match = products[top_indices[0].item()]

    # Optional: log similarity scores for debugging
    for idx, i in enumerate(top_indices):
        print(f"Rank {idx+1}: {products[i.item()].name} (score: {similarities[i].item():.4f})")

    # Return the top products, closest match, and fallback suggestions
    return {
        "products": [{"id": p.id, "name": p.name, "description": p.description} for p in top_products],
        "closest_item": {
            "id": closest_match.id,
            "name": closest_match.name,
            "score": round(closest_score, 2),
            "explanation": "This matched your query best based on semantic similarity."
        },
        "fallback_suggestions": None if closest_score > 0.3 else [
            "Try searching more broadly",
            "Check spelling or use fewer words"
        ]
    }


# Generate recommendations based on a user query
async def generate_recommendations(payload: RecommendRequest, db: AsyncSession) -> list[str]:
    """
    Generate personalized product recommendations based on a user query.

    Args:
        payload (RecommendRequest): The recommendation request containing the query.
        db (AsyncSession): The database session for querying products.

    Returns:
        list[str]: A list of recommended product names or fallback suggestions.
    """
    try:
        # Extract the query string from the payload
        prompt = payload.query  # Access the `query` attribute of the RecommendRequest object

        # Retrieve top products based on the query
        result = await retrieve_top_products(prompt, db)

        # Handle the case where no products match the query
        if not result["products"]:
            return ["Sorry, we couldn't find any good matches!"] + (result["fallback_suggestions"] or [])

        # Prepare product names for the T5 model
        product_names = ", ".join([p["name"] for p in result["products"]])
        final_prompt = f"User wants: {prompt}. Recommend these: {product_names}."

        # Generate recommendations using the T5 model
        input_ids = tokenizer(final_prompt, return_tensors="pt").input_ids
        outputs = t5_model.generate(input_ids, max_length=64, num_beams=4, early_stopping=True)

        # Decode the output and split it into a list of recommendations
        recommendation_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        recommendations = [rec.strip() for rec in recommendation_text.split(",")]

        return recommendations

    except Exception as e:
        # Log the error and return a fallback message
        print("🔥 ERROR in generate_recommendations:", e)
        return ["Oops! Something went wrong while generating recommendations."]
