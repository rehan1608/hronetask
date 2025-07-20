from db.mongodb import MongoDB
from models.product import ProductCreate, ProductResponse
from models.pagination import PaginatedResponse, Page
from typing import List, Optional
from bson import ObjectId

class ProductService:
    def __init__(self):
        self.collection = MongoDB.database["products"]

    def create_product(self, product: ProductCreate) -> str:
        product_data = product.model_dump()
        result = self.collection.insert_one(product_data)
        return str(result.inserted_id)

    def list_products(self, name: Optional[str] = None, size: Optional[str] = None, limit: int = 10, offset: int = 0) -> PaginatedResponse:
        query = {}
        if name:
            query["name"] = {"$regex": name, "$options": "i"} # Case-insensitive partial search 
        if size:
            query["sizes.size"] = size # Filter by size
        total_products = self.collection.count_documents(query)
        
        # Sort by _id for consistent pagination
        products_cursor = self.collection.find(query, {"name": 1, "price": 1}).sort("_id").skip(offset).limit(limit)
        
        products = []
        for product in products_cursor:
            products.append(ProductResponse(_id=str(product["_id"]), name=product["name"], price=product["price"]))
        
        next_offset = offset + limit if offset + limit < total_products else None
        previous_offset = offset - limit if offset - limit >= 0 else None

        # Convert next_offset and previous_offset to string for consistency with example
        next_page_str = str(next_offset) if next_offset is not None else None
        previous_page_str = str(previous_offset) if previous_offset is not None else None
        
        page_info = Page(
            next=next_page_str,
            limit=len(products),
            previous=previous_page_str
        )
        return PaginatedResponse(data=products, page=page_info)