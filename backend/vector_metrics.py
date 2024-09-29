import os
import requests

model_id = "sentence-transformers/all-MiniLM-L6-v2"
hf_token=os.environ.get("HF")

api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
headers = {"Authorization": f"Bearer {hf_token}"}

def query_for_embedding(review):
    response = requests.post(api_url, headers=headers, json={"inputs": review, "options":{"wait_for_model":True}})
    return response.json()
