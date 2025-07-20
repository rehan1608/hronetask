# HROne E-commerce Backend Intern Task

This project implements a sample backend application for an e-commerce platform using FastAPI and MongoDB, as per the HROne Backend Intern Hiring Task.

## Features

* **Create Product API**: Allows adding new products with name, price, and different sizes/quantities.
* **List Products API**: Retrieves a list of products with optional filtering by name (partial/regex) and size, and supports pagination.
* **Create Order API**: Enables users to create orders specifying the products and quantities.
* **Get List of Orders API**: Fetches orders for a specific user, including detailed product information (lookup/join from products collection), with pagination.

## Tech Stack

* **Python 3.10+**
* **FastAPI**: For building the RESTful APIs.
* **MongoDB Atlas**: As the NoSQL database for data storage.
* **Pymongo**: Python driver for MongoDB.
* **Uvicorn**: ASGI server to run the FastAPI application.
* **python-dotenv**: For managing environment variables.

## Project Structure
```
hronetask/
├── .env                    # Environment variables (e.g., MongoDB URI)
├── main.py                 # Main FastAPI application entry point
├── models/
│   ├── product.py          # Pydantic models for Product schema
│   ├── order.py            # Pydantic models for Order schema
│   └── pagination.py       # Pydantic models for Pagination schema
├── db/
│   └── mongodb.py          # MongoDB connection and client management
├── routers/
│   ├── product_router.py   # API endpoints for Products
│   └── order_router.py     # API endpoints for Orders
├── services/
│   ├── product_service.py  # Business logic for Products
│   └── order_service.py    # Business logic for Orders
└── README.md               # This README file
└── requirements.txt        # Python dependencies
```
## Setup and Run Locally

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd hronetask
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure MongoDB:**
    * Set up a free tier MongoDB Atlas cluster.
    * Obtain your MongoDB connection URI.
    * Create a `.env` file in the project root and add your MongoDB URI:
        ```
        MONGO_URI="mongodb+srv://<your_username>:<your_password>@cluster0.abcde.mongodb.net/?retryWrites=true&w=majority"
        ```
        Replace `<your_username>` and `<your_password>` with your actual MongoDB Atlas credentials.

5.  **Run the application:**
    ```bash
    python main.py
    ```
    The application will run on `http://0.0.0.0:8000`.

## API Documentation

Once the application is running, you can access the interactive API documentation (Swagger UI) at:
`http://localhost:8000/docs`

## Deployment (Render/Railway)

This application is designed to be deployable on platforms like Render or Railway.

1.  **Push your code to GitHub:**
    Make sure your repository is public or you've granted access to `shreybatra`.

2.  **Create a new web service on Render/Railway:**
    * Connect your GitHub repository.
    * Set the build command (e.g., `pip install -r requirements.txt`).
    * Set the start command (e.g., `uvicorn main:app --host 0.0.0.0 --port $PORT`).
    * Add your `MONGO_URI` as an environment variable in the Render/Railway dashboard settings.

3.  **Provide the base URL:**
    After successful deployment, Render/Railway will provide a public URL for your application. This is the base URL you need to submit (e.g., `https://your-app-name.onrender.com`).

## API Endpoints

### 1. Create Product API

* **Endpoint**: `/products`
* **Method**: `POST`
* **Request Body**:
    ```json
    {
      "name": "string",
      "price": 100.0,
      "sizes": [
        {
          "size": "string",
          "quantity": 0
        }
      ]
    }
    ```
* **Response Body**:
    ```json
    {
      "id": "1234567890"
    }
    ```
* **Status Code**: `201 CREATED`

### 2. List Products API

* **Endpoint**: `/products`
* **Method**: `GET`
* **Query Parameters (Optional)**:
    * `name`: string (partial search, e.g., `?name=sample`)
    * `size`: string (filter by size, e.g., `?size=large`)
    * `limit`: int (number of documents to return, default 10)
    * `offset`: int (number of documents to skip, default 0)
* **Response Body**:
    ```json
    {
      "data": [
        {
          "id": "12345",
          "name": "Sample",
          "price": 100.0
        },
        {
          "id": "12346",
          "name": "Sample 2",
          "price": 10.0
        }
      ],
      "page": {
        "next": "10",
        "limit": 0,
        "previous": "-10"
      }
    }
    ```
* **Status Code**: `200 OK`

### 3. Create Order API

* **Endpoint**: `/orders`
* **Method**: `POST`
* **Request Body**:
    ```json
    {
      "userId": "user_1",
      "items": [
        {
          "productId": "123456789",
          "qty": 3
        },
        {
          "productId": "2222222",
          "qty": 3
        }
      ]
    }
    ```
* **Response Body**:
    ```json
    {
      "id": "1234567890"
    }
    ```
* **Status Code**: `201 CREATED`

### 4. Get List of Orders API

* **Endpoint**: `/orders/{user_id}`
* **Method**: `GET`
* **URL Parameter**:
    * `user_id`: string (e.g., `user_1`)
* **Query Parameters (Optional)**:
    * `limit`: int (number of documents to return, default 10)
    * `offset`: int (number of documents to skip, default 0)
* **Response Body**:
    ```json
    {
      "data": [
        {
          "id": "12345",
          "items": [
            {
              "productId": "123456",
              "qty": 3,
              "productDetails": {
                "id": "123456",
                "name": "Sample Product"
              }
            },
            {
              "productId": "222222",
              "qty": 3,
              "productDetails": {
                "id": "222222",
                "name": "Another Product"
              }
            }
          ],
          "total": 250.0
        }
      ],
      "page": {
        "next": "10",
        "limit": 0,
        "previous": "-10"
      }
    }
    ```
* **Status Code**: `200 OK`

## MongoDB Collection Structure

### `products` Collection

Documents will look like:

```json
{
  "_id": ObjectId("60c72b2f9b1e8e2b2c3d4e5f"),
  "name": "T-Shirt",
  "price": 25.99,
  "sizes": [
    {
      "size": "small",
      "quantity": 50
    },
    {
      "size": "medium",
      "quantity": 100
    },
    {
      "size": "large",
      "quantity": 75
    }
  ]
}
```
### `Orders` Collection
Documents will look like:
```json
{
  "_id": ObjectId("60c72b2f9b1e8e2b2c3d4e60"),
  "userId": "user_1",
  "items": [
    {
      "productId": "60c72b2f9b1e8e2b2c3d4e5f",
      "qty": 2
    },
    {
      "productId": "60c72b2f9b1e8e2b2c3d4e61",
      "qty": 1
    }
  ],
  "total": 75.97
}
```
During the Get List of Orders API call, a `$lookup` aggregation pipeline will be used to fetch productDetails from the products collection based on productId.
