from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def connect_to_mongo():
    try:
        uri = os.getenv('MONGODB_URI')  # Use your MongoDB Atlas connection string here
        client = MongoClient(uri)
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None