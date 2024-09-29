from flask import Flask, request, jsonify
from inference import get_product_and_description_from_url, get_questions_for_product  # Import your AI generation function
from product import insert_if_not_exists, find_by_url  # MongoDB functions
from inference import enhance_question, categorize_review
from vector_metrics import query_for_embedding
from pymongo_connection import connect_to_mongo
import time
import json

app = Flask(__name__)
client = connect_to_mongo

@app.route('/')
def index():
    return "welcome to the index page"

@app.route('/process_product', methods=['POST'])
def process_product():
    print("request.json")
    """Process the product URL: scrape if not in DB, then retrieve and return questions."""
    data = request.json
    product_url = data.get('url')

    if not product_url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        # Step 1: Connect to Mongo
        if not client:
            return jsonify({"error": "Failed to connect to MongoDB"}), 500
        # Step 2: Check if the product already exists in MongoDB
        existing_product = find_by_url(client, 'review-db', 'products', product_url)

        if not existing_product:
            # Step 3: scrape product and description
            prod_entry = get_product_and_description_from_url(product_url)
            if not prod_entry:
                return jsonify({"error": "Failed to scrape product info"}), 500

            # Step 4: Use AI to generate additional info
            document = get_questions_for_product(prod_entry)

            # Step 5: Insert the new product into MongoDB
            insert_result, insert_status_code = insert_if_not_exists(client, 'review-db', 'products', document)
            if insert_status_code != 201:
                return jsonify({"error": "Failed to insert new product"}), 500

        # Step 7: Retrieve the product again (whether it was inserted or already existed)
        product = find_by_url(client, 'review-db', 'products', product_url)
        if not product or 'questions' not in product:
            return jsonify({"error": "Product not found or no questions available"}), 500

        # Step 8: Extract the first 3 questions using keys like q1, q2, q3
        questions_field = product.get('questions', {})
        questions = [questions_field.get(f'q{i}') for i in range(1, 4) if questions_field.get(f'q{i}')]

        return jsonify({"questions": questions})

    except Exception as e:
        print(f"Error processing the product: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/submit_review', methods=['POST'])
def submit_review():
    """Receive URL, review, rating; generate review embedding, and insert into MongoDB."""
    data = request.json
    product_url = data.get('url')
    review = data.get('review')
    rating = data.get('rating')

    if not product_url or not review or not rating:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Step 2: Connect to MongoDB
        if not client:
            return jsonify({"error": "Failed to connect to MongoDB"}), 500

        # Step 3: Prepare the document for insertion
        review_document = {
            "url": product_url,
            "review": review,
            "rating": rating,
            "category": categorize_review(review, ["durability", "affordibility", "accessibility", "versatility"])
        }

        # Step 4: Insert the review into MongoDB
        db = client['review-db']
        collection = db['reviews'] 
        insert_result = collection.insert_one(review_document)
        collection.find()
        
        return jsonify({"message": "Review submitted"}), 201

    except Exception as e:
        print(f"Error submitting review: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/search_review', methods=['POST'])
def search_review():
    data = request.json
    product_url = data.get('url')
    question = data.get('question')
    query = {"url": product_url}
    user_selected_category = data.get('category')
    all_intended_reviews = []
    
    # Find the document
    try:
        # Connect to MongoDB
        if not client:
            return jsonify({"error": "Failed to connect to MongoDB"}), 500
        
        db = client['review-db']
        collection = db['reviews'] 
        # collection.find({"field1": "value1", "field2": "value2"})
        documents = collection.find({"category": user_selected_category, "url": product_url})
        all_intended_reviews = []
        for doc in documents:
            review = doc.get('review', "")
            all_intended_reviews.append(review)
        return json.dumps(all_intended_reviews)
       
     
        
    except Exception as e:
        print(e)
        return None
    

if __name__ == "__main__":
    app.run(port=5000, debug=True)