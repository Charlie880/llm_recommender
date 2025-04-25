from pydantic import BaseModel

# Schema for recommendation request
class RecommendRequest(BaseModel):
    """
    Represents the schema for a recommendation request.

    This schema is used to validate the input data when a user
    requests product recommendations.
    """
    
    query: str  # Query or search term for recommendations

# Schema for recommendation response
class RecommendResponse(BaseModel):
    """
    Represents the schema for a recommendation response.

    This schema is used to structure the response data sent back
    to the client after processing a recommendation request.
    """

    recommendations: list[str]  # List of recommended product names or items    recommendations: list[str]  # List of recommended product names or items
