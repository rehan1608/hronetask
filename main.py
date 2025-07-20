from fastapi import FastAPI
from routers import product_router, order_router
from db.mongodb import MongoDB
import uvicorn
import os

app = FastAPI(
    title="HROne E-commerce Backend",
    description="A sample backend application for an e-commerce platform.",
    version="1.0.0",
)

# Include routers
app.include_router(product_router.router)
app.include_router(order_router.router)

@app.on_event("startup")
async def startup_event():
    """
    Connect to MongoDB on application startup.
    """
    MongoDB.connect()

@app.on_event("shutdown")
async def shutdown_event():
    """
    Close MongoDB connection on application shutdown.
    """
    MongoDB.close()

@app.get("/")
async def root():
    return {"message": "Welcome to HROne E-commerce API! Visit /docs for API documentation."}

if __name__ == "__main__":
    if os.getenv("MONGO_URI") is None:
        print("Warning: MONGO_URI environment variable is not set. Please set it in .env or your environment.")
    uvicorn.run(app, host="0.0.0.0", port=8000)