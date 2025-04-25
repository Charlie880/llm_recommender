from sentence_transformers import SentenceTransformer, util
import torch
from app.models.product import Product  # SQLAlchemy model

# Load the sentence-transformer model (this may take a few seconds at startup)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_top_products(query: str, db, top_k: int = 3) -> list[Product]:
    """
    Retrieve the top_k products from the database that are semantically similar
    to the user query.

    Args:
        query (str): The user's search query.
        db: The database session for querying products.
        top_k (int): The maximum number of top products to retrieve.

    Returns:
        list[Product]: A list of Product objects that are most similar to the query.
    """
    # Query all products from the database
    products = db.query(Product).all()
    if not products:
        # Return an empty list if no products are available
        return []
    
    # Prepare product texts for embedding ("Product name: description")
    # If a product has no description, only the name is used
    product_texts = [f"{p.name}: {p.description}" for p in products]

    # Compute embeddings for the query and product texts
    query_embedding = embedder.encode(query, convert_to_tensor=True)  # Query embedding
    product_embeddings = embedder.encode(product_texts, convert_to_tensor=True)  # Product embeddings

    # Calculate cosine similarity between the query and each product embedding
    similarities = util.cos_sim(query_embedding, product_embeddings)[0]

    # Get indices of the top_k most similar products
    top_indices = torch.topk(similarities, k=min(top_k, len(products))).indices

    # Retrieve the corresponding Product objects based on the top indices
    top_products = [products[i] for i in top_indices]

    # Return the list of top Product objects
    return top_products
