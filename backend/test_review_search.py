from flask import Flask, request, jsonify
from inference import get_product_and_description_from_url, get_questions_for_product  # Import your AI generation function
from product import insert_if_not_exists, find_by_url  # MongoDB functions
from pymongo_connection import connect_to_mongo
from inference import enhance_question
from vector_metrics import query_for_embedding
from inference import categorize_review
import time
#from pinecone import Pinecone, ServerlessSpec
import json

def test_script():
    durability_reviews = [
    "I've been using these shoes for months, and they are still holding up great. The durability is impressive, even after constant use on the court.",
    "Not happy with how quickly these shoes wore out. After just a few games, the soles are already starting to come apart.",
    "I can’t believe how long these shoes have lasted! I’ve played in them every weekend, and they still feel as solid as the first day I wore them.",
    "The shoes were decent, but after about two months, they started to show signs of wear and tear. Definitely not as durable as I had hoped.",
    "These shoes are built like a tank! I've played on rough outdoor courts, and they've held up amazingly well."
]
    price_reviews = [
    "These shoes are way overpriced for what you get. The design is nice, but I don’t think they’re worth the money.",
    "I love the look and style of these shoes, but they definitely aren’t budget-friendly. You can find similar shoes for a lower price.",
    "While they perform well on the court, the price tag is just too high. I don’t think they offer good value for the cost.",
    "The fit is okay, but I expected more comfort given the price point. They’re not as cushioned as I hoped they would be.",
    "Honestly, I bought these just because they look cool. I don’t care much about the performance, but the aesthetic is top-notch."
]
    
    categories = ['price', 'durability', 'aesthetic']
    client = connect_to_mongo()
    if not client:
        return jsonify({"error": "Failed to connect to MongoDB"}), 500
    
    for review in durability_reviews:
        # Step 3: Prepare the document for insertion
        review_document = {
            "url": "xyz.com",
            "review": review,
            "rating": 5,
            "category": categorize_review(review, categories)
        }

        # Step 4: Insert the review into MongoDB
        db = client['review-db']
        collection = db['reviews'] 
        insert_result = collection.insert_one(review_document)
        
    
    for review in price_reviews:
        # Step 3: Prepare the document for insertion
        review_document = {
            "url": "xyz.com",
            "review": review,
            "rating": 5,
            "category": categorize_review(review, categories)
        }

        # Step 4: Insert the review into MongoDB
        db = client['review-db']
        collection = db['reviews'] 
        insert_result = collection.insert_one(review_document)
    

    

    # question = "How long do these shoes last?"
    # user_selected_category = "durability"
    # query = {"url": 'xyz.com'}

    # db = client['review-db']
    # collection = db['reviews'] 
    # # collection.find({"field1": "value1", "field2": "value2"})
    # documents = collection.find({"category": user_selected_category, "url": "xyz.com"})
    # all_intended_reviews = []
    # for doc in documents:
    #     review = doc.get('review', "")
    #     all_intended_reviews.append(review)
    # print(all_intended_reviews)
    #return json.dumps(all_intended_reviews)
    return None

def insert_xyz():
    client = connect_to_mongo()
    url="https://kith.com/collections/kith-footwear/products/x2j162xf85500"
    prod_entry = get_product_and_description_from_url(url)
    final_entry = get_questions_for_product(prod_entry)
    final_entry['url'] = 'xyz.com'
    insert_if_not_exists(client, 'review-db', 'products', final_entry)

if __name__ == "__main__":
    #test_script()
    insert_xyz()