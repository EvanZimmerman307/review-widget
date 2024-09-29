import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo_connection import connect_to_mongo
from inference import get_product_and_description_from_url, get_questions_for_product, generate_example_review
from product import insert_if_not_exists, find_by_url
from vector_metrics import query_for_embedding

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


# Retrieve MongoDB credentials from environment variables


client = connect_to_mongo
"""Establishes a connection to MongoDB."""
try:
    client.admin.command('ping')  # Test connection
    print("Successfully connected to MongoDB.")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

@app.before_request
def log_request_info():
    print('Headers: %s', request.headers)
    print('Body: %s', request.get_data())

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


@app.route('/process_product', methods=['POST', 'OPTIONS'])
def process_product():
    if request.method == 'OPTIONS':
        # Preflight request:
        response = jsonify({'status': 'Options Request'})
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response, 200

    """Process the product URL: scrape if not in DB, then retrieve and return questions."""
    data = request.json
    product_url = data.get('url')

    if not product_url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        # Step 1: Connect to MongoDB
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

@app.route('/submit_review', methods=['POST', 'OPTIONS'])
def submit_review():
    if request.method == 'OPTIONS':
        # Preflight request:
        response = jsonify({'status': 'Options Request'})
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response, 200

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
            "embedding": query_for_embedding(review)
        }

        # Step 4: Insert the review into MongoDB
        db = client['review-db']
        collection = db['reviews']
        collection.insert_one(review_document)

        # Step 5: Return success message
        response = jsonify({"message": "Review submitted"})
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        return response, 201

    except Exception as e:
        print(f"Error submitting review: {e}")
        response = jsonify({"error": str(e)})
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        return response, 500

@app.route('/search_review', methods=['POST'])
def search_review():
    # get the data
    """Receive URL, review"""
    data = request.json
    product_url = data.get('url')
    review = data.get('review')
    # category = data.get('category') # use this to generate relevant sample reviews

    #receive item name and sentiment category (e.g. blender and / durability?)
    # create a monogodb index in dashboard to find most similar embedding
    # generate a review about this item that covers this category
    # do the vector search
    # return the review we just generated
    # computing vector embeddings that max out the category

if __name__ == "__main__":
    app.run(port=5000, debug=True)