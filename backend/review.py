import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from product import connect_to_mongo

# Load environment variables from a .env file
load_dotenv()

# Retrieve MongoDB credentials from environment variables
DB_NAME = "review-db" 
COLLECTION_NAME = "reviews"

def insert_review(client, db_name, collection_name, document):
    """
    - document contains
        url (from frontend)
        review(from frontend)
        rating(from frontend)
        embedding(from backend)
    """
    db = client[db_name]
    collection = db[collection_name]

    try:
        result = collection.insert_one(document)
        print(f"Inserted document with ID: {result.inserted_id}")
    except Exception as e:
        print(f"Error inserting document: {e}")

def main():
    # Connect to MongoDB
    client = connect_to_mongo()

    if client:
        document = {
            "url": "some url",
            "review": "this product sucks",
            "rating": 5,
            "embedding": [1,2,3,4,5]
        }
        insert_review(client, DB_NAME, COLLECTION_NAME, document)

if __name__ == "__main__":
    main()