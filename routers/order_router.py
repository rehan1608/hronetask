from fastapi import APIRouter, status, Query, Path
from models.order import OrderCreate, OrderResponse
from models.pagination import PaginatedResponse
from services.order_service import OrderService
from typing import Optional

router = APIRouter()
order_service = OrderService()

@router.post("/orders", status_code=status.HTTP_201_CREATED)
async def create_order_api(order: OrderCreate):
    """
    Create Order API
    """
    order_id = order_service.create_order(order)
    # The problem statement response is {"$id": "1234567890"}
    return {"id": order_id}

@router.get("/orders/{user_id}", response_model=PaginatedResponse, status_code=status.HTTP_200_OK)
async def get_list_of_orders_api(
    user_id: str = Path(..., description="The ID of the user whose orders to retrieve"),
    limit: int = Query(10, ge=1, description="Number of documents to return "),
    offset: int = Query(0, ge=0, description="Number of documents to skip while paginating (sorted by _id)")
):
    """
    Get List of Orders API
    """
    return order_service.get_user_orders(user_id=user_id, limit=limit, offset=offset)