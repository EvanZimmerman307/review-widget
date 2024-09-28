import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from a .env file
load_dotenv()

# Retrieve MongoDB credentials from environment variables
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = "review-db" 
COLLECTION_NAME = "products"

# OpenAI API key
#openai_api_key = os.environ.get("OPENAI_API_KEY")
#print(os.environ.get("OPENAI_API_KEY"))


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

#def generate_questions(name, description, num_questions=3):
    """
    Generates questions prompting a user review based on the product name and description.

    Args:
        name (str): The product name.
        description (str): The product description.
        num_questions (int): The number of questions to generate.

    Returns:
        list: A list of generated questions.
    """
    prompt = (
        f"Based on the following product name and description, generate {num_questions} questions "
        f"that would prompt a user to provide a detailed review:\n\n"
        f"Product Name: {name}\n"
        f"Product Description: {description}\n\nQuestions:"
    )

    try:
        model = "gpt-4o" 
        response = open_ai_client.chat.completions.create(
            messages=[
                { "role": "system", "content": "You are an AI assistant that generates review questions."},
                {"role": "user", "content": prompt}
            ],
            model=model
        )

        # Extract the generated text
        generated_text = response.choices[0].message.content
        #print(generated_text)

        # Split the generated text into individual questions
        generated_text = generated_text.split('\n')
        # Remove empty strings
        questions = [item for item in generated_text if item]

        return questions[:num_questions]

    except Exception as e:
        print(f"Error generating questions: {e}")
        return []

def insert_if_not_exists(client, db_name, collection_name, document):
    """Checks if a document exists in the collection and inserts if not."""
    db = client[db_name]
    collection = db[collection_name]

    # Check if document exists based on the 'url'
    query = {"url": document["url"]}
    existing_doc = collection.find_one(query)
    #questions = generate_questions(document["name"], document["description"])

    if existing_doc:
        print(f"Document already exists: {existing_doc}")
    else:
        # Generate questions based on the name and description
        #questions = generate_questions(document["name"], document["description"])
        #document["questions"] = questions
        try:
            result = collection.insert_one(document)
            print(f"Inserted document with ID: {result.inserted_id}")
        except Exception as e:
            print(f"Error inserting document: {e}")

def main():
    # Connect to MongoDB
    client = connect_to_mongo()

    if client:
        # Example product document
        document = {
            "url": "https://example.com/product123",
            "name": "Wireless Headphones",
            "description": "Experience crystal clear sound with our Wireless Headphones featuring noise-cancellation and long-lasting battery life.",
            # 'questions' field will be populated by generate_questions()
        }

        # Insert product if it doesn't exist
        insert_if_not_exists(client, DB_NAME, COLLECTION_NAME, document)


if __name__ == "__main__":
    main()
