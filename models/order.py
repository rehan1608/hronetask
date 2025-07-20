# models/order.py
from pydantic import BaseModel, Field
from typing import List, Optional

class OrderItemRequest(BaseModel):
    productId: str
    qty: int

class OrderCreate(BaseModel):
    userId: str # Can be hardcoded as "user_1" [cite: 7]
    items: List[OrderItemRequest]

class ProductDetails(BaseModel):
    id: str = Field(alias="_id")
    name: str

    class Config:
        populate_by_name = True

class OrderItemResponse(BaseModel):
    productId: str # This is the productId from the request
    qty: int
    productDetails: ProductDetails # We need to join/lookup the product details at query time [cite: 8]

class OrderResponse(BaseModel):
    id: str = Field(alias="_id") # Order ID [cite: 8]
    items: List[OrderItemResponse]
    total: float

    class Config:
        populate_by_name = True