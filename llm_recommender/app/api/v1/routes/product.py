from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import get_async_session  # Asynchronous DB session
from app.models.product import Product  # Product model
from app.schemas.product import ProductOut #ProductCreate

# Define the router for product-related endpoints
router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=list[ProductOut])
async def list_products(session: AsyncSession = Depends(get_async_session)):
    """
    Retrieve a list of all products.

    Args:
        session (AsyncSession): The database session dependency.

    Returns:
        list[ProductOut]: A list of products in the database.
    """
    # Execute a query to select all products from the database
    result = await session.execute(select(Product))
    products = result.scalars().all()  # Retrieve all product objects
    return products  # Return the list of products

# @router.post("/", response_model=ProductOut)
# async def create_product(
#     payload: ProductCreate,
#     session: AsyncSession = Depends(get_async_session),
# ):
#     """
#     Create a new product in the database.

#     Args:
#         payload (ProductCreate): The product data to create.
#         session (AsyncSession): The database session dependency.

#     Returns:
#         ProductOut: The newly created product.
#     """
#     # Create a new Product object from the payload
#     new_product = Product(**payload.dict())
#     session.add(new_product)  # Add the product to the session
#     await session.commit()  # Commit the transaction to save the product
#     await session.refresh(new_product)  # Refresh the product to get updated data
#     return new_product  # Return the newly created product