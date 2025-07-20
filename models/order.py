from pydantic import BaseModel, Field
from typing import List, Optional

class OrderItemRequest(BaseModel):
    productId: str = Field(alias="productId")
    qty: int

class OrderCreate(BaseModel):
    userId: str 
    items: List[OrderItemRequest]

class ProductDetails(BaseModel):
    id: str = Field(alias="_id")
    name: str

    class Config:
        populate_by_name = True

class OrderItemResponse(BaseModel):
    productId: str = Field(alias="productId") # This is the productId from the request
    qty: int
    productDetails: ProductDetails # We need to join/lookup the product details at query time 

class OrderResponse(BaseModel):
    id: str = Field(alias="_id") # Order ID 
    items: List[OrderItemResponse]
    total: float

    class Config:
        populate_by_name = True