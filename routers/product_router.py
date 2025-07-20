# routers/product_router.py
from fastapi import APIRouter, status, Query
from models.product import ProductCreate, ProductResponse
from models.pagination import PaginatedResponse
from services.product_service import ProductService
from typing import Optional

router = APIRouter()
product_service = ProductService()

@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product_api(product: ProductCreate):
    """
    Create Products API
    """
    product_id = product_service.create_product(product)
    # The problem statement response is {"id": "1234567890"} [cite: 5]
    # Pydantic ProductResponse expects an _id for its alias 'id'
    return ProductResponse(_id=product_id, name=product.name, price=product.price) # Return a minimal ProductResponse based on spec [cite: 5]

@router.get("/products", response_model=PaginatedResponse, status_code=status.HTTP_200_OK)
async def list_products_api(
    name: Optional[str] = Query(None, description="Partial search by product name"),
    size: Optional[str] = Query(None, description="Filter by product size"),
    limit: int = Query(10, ge=1, description="Number of documents to return [cite: 6]"),
    offset: int = Query(0, ge=0, description="Number of documents to skip while paginating (sorted by _id) [cite: 6]")
):
    """
    List Products API
    """
    return product_service.list_products(name=name, size=size, limit=limit, offset=offset)