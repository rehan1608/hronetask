from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
from dotenv import load_dotenv

load_dotenv()

class MongoDB:
    client: MongoClient = None
    database = None

    @staticmethod
    def connect():
        if MongoDB.client is None:
            MONGO_URI = os.getenv("MONGO_URI")
            if not MONGO_URI:
                raise ValueError("MONGO_URI environment variable not set.")
            try:
                MongoDB.client = MongoClient(MONGO_URI)
                MongoDB.database = MongoDB.client["hronedb"]  # Choose your database name
                # The ismaster command is cheap and does not require auth.
                MongoDB.client.admin.command('ismaster')
                print("MongoDB connected successfully!")
            except ConnectionFailure as e:
                print(f"Could not connect to MongoDB: {e}")
                MongoDB.client = None
            except Exception as e:
                print(f"An unexpected error occurred during MongoDB connection: {e}")

    @staticmethod
    def close():
        if MongoDB.client:
            MongoDB.client.close()
            MongoDB.client = None
            print("MongoDB connection closed.")

# Initialize connection on application startup
MongoDB.connect()