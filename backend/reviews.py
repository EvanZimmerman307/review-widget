import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Retrieve MongoDB credentials from environment variables
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = "review-db" 
COLLECTION_NAME = "reviews"

def connect_to_mongo():
    """Establishes a connection to MongoDB."""
    try:
        client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
        client.admin.command('ping')  # Test connection
        print("Successfully connected to MongoDB.")
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None


def insert(client, db_name, collection_name, document):
    """
    - insert this review into the database
    - columns: url, review, rating
    """
    db = client[db_name]
    collection = db[collection_name]


    if existing_doc:
        print(f"Document already exists: {existing_doc}")
    else:
        # Generate questions based on the name and description
        questions = generate_questions(document["name"], document["description"])
        document["questions"] = questions
        try:
            result = collection.insert_one(document)
            print(f"Inserted document with ID: {result.inserted_id}")
        except Exception as e:
            print(f"Error inserting document: {e}")
