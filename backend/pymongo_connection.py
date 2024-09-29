from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

def connect_to_mongo():
    try:
        mongo_uri = os.getenv("MONGO_URI")
        client = MongoClient(mongo_uri)
        db = client['your_database_name']
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None