from db.mongodb import MongoDB
from models.order import OrderCreate, OrderResponse, OrderItemResponse, ProductDetails
from models.pagination import PaginatedResponse, Page
from typing import List, Optional
from bson import ObjectId

class OrderService:
    def __init__(self):
        self.orders_collection = MongoDB.database["orders"]
        self.products_collection = MongoDB.database["products"]

    def create_order(self, order: OrderCreate) -> str:
        order_data = order.model_dump()

        total_price = 0.0
        for item in order_data["items"]:
            # Let's fetch product price to calculate total accurately
            product_id_obj = ObjectId(item["productId"])
            product_info = self.products_collection.find_one({"_id": product_id_obj}, {"price": 1})
            if product_info :
                total_price += product_info["price"] * item["qty"]
            else:
                # Handle case where product is not found, e.g., raise an error or skip
                print(f"Product with ID {item['productId']} not found for order.")

        order_data["total"] = total_price
        result = self.orders_collection.insert_one(order_data)
        return str(result.inserted_id)

    def get_user_orders(self, user_id: str, limit: int = 10, offset: int = 0) -> PaginatedResponse:
        query = {"userId": user_id}

        total_orders = self.orders_collection.count_documents(query)

        # We need to join/lookup the product details at query time
        # Using aggregation pipeline for lookup
        pipeline = [
            {"$match": {"userId": user_id}},
            {"$sort": {"_id": 1}}, # Sorted by _id for pagination 
            {"$skip": offset},
            {"$limit": limit},
            {"$unwind": "$items"}, # Deconstruct the items array
            {"$addFields": {
                "items.productId_obj": { "$toObjectId": "$items.productId" }
            }},
            {"$lookup": {
                "from": "products", # The collection to join with
                "localField": "items.productId_obj", # Field from the input documents
                "foreignField": "_id", # Field from the "products" documents
                "as": "items.productDetails" # Output array field
            }},
            {"$unwind": "$items.productDetails"}, # Deconstruct the productDetails array
            {"$group": {
                "_id": "$_id",
                "userId": {"$first": "$userId"},
                "total": {"$first": "$total"},
                "items": {"$push": {
                    "productId": "$items.productId",
                    "qty": "$items.qty",
                    "productDetails": {
                        "_id": "$items.productDetails._id",
                        "name": "$items.productDetails.name"
                    }
                }}
            }},
            {"$project": {
                "_id": 1,
                "items": 1,
                "total": 1,
                "userId": 1
            }}
        ]
        

        orders_cursor = self.orders_collection.aggregate(pipeline)
        
        orders = []
        for order_doc in orders_cursor:
            items_response = []
            for item in order_doc["items"]:
                product_details_obj = ProductDetails(
                    _id=str(item["productDetails"]["_id"]),
                    name=item["productDetails"]["name"]
                )
                items_response.append(OrderItemResponse(
                    productId=str(item["productId"]), # Ensure productId is string
                    qty=item["qty"],
                    productDetails=product_details_obj
                ))
            orders.append(OrderResponse(
                _id=str(order_doc["_id"]),
                items=items_response,
                total=order_doc["total"]
            ))

        next_offset = offset + limit if offset + limit < total_orders else None
        previous_offset = offset - limit if offset - limit >= 0 else None
        
        next_page_str = str(next_offset) if next_offset is not None else None
        previous_page_str = str(previous_offset) if previous_offset is not None else None

        page_info = Page(
            next=next_page_str,
            limit=len(orders),
            previous=previous_page_str
        )
        return PaginatedResponse(data=orders, page=page_info)