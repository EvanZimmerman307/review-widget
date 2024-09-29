"""
mongodb+srv://evanzimm:<db_password>@review-widget.o43vfpw.mongodb.net/?retryWrites=true&w=majority&appName=review-widget
"""

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://evanzimm:jszMxdrSo9ghCIb5@review-widget.o43vfpw.mongodb.net/?retryWrites=true&w=majority&appName=review-widget"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Step 2: Access (or create) a database. This won't create the database yet.
db = client['review-db']

# Step 3: Access (or create) a collection. The database and collection are created when data is inserted.
collection = db['products']

# Step 4: Insert a document (this will create the database and collection if they don't exist)
document = {
  "url": "link",
  "name": "product",
  "description": "product description",
  "questions": [
    "question1",
    "question2",
    "question3"
  ]
}

query = {"url": "link"}

document = collection.find_one(query)

# Step 4: Check the result
if document:
    print(f"Document exists: {document}")
else:
    print("Document does not exist.")
    # Insert the document
    result = collection.insert_one(document)
    # Step 5: Print the inserted ID
    print(f"Inserted document ID: {result.inserted_id}")






