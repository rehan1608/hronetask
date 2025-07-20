from pydantic import BaseModel, Field
from typing import List, Optional

class ProductSize(BaseModel):
    size: str
    quantity: int

class ProductCreate(BaseModel):
    name: str
    price: float
    sizes: List[ProductSize]

class ProductResponse(BaseModel):
    id: str = Field(alias="_id") # Alias for MongoDB's _id
    name: str
    price: float

    class Config:
        populate_by_name = True # Allow population by field name or alias
        json_encoders = {
            # Custom encoder for ObjectId if you are returning full MongoDB objects
            # but for this task, we will convert ObjectId to str explicitly
        }