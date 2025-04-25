from pydantic import BaseModel

# Base schema for Product
class ProductBase(BaseModel):
    """
    Represents the base schema for a product.

    This schema includes common fields shared across different
    product-related operations, such as name, description, and price.
    """
    name: str  # Name of the product
    description: str  # Description of the product
    price: float  # Price of the product

# # Schema for creating a new product
# class ProductCreate(ProductBase):
#     """
#     Schema for creating a new product.

#     Inherits all fields from ProductBase. Additional fields can
#     be added here if needed for product creation.
#     """
#     pass

# Schema for returning product data to the client
class ProductOut(ProductBase):
    """
    Schema for returning product data to the client.

    Includes all fields from ProductBase and adds the product ID.
    """
    id: int  # Unique identifier for the product

    class Config:
        """
        Configuration for the Pydantic model.

        Enables ORM mode to allow compatibility with SQLAlchemy models.
        """
        from_attributes = True
