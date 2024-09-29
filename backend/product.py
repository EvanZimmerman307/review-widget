import os
from inference import get_product_and_description_from_url, get_questions_for_product
from pymongo_connection import connect_to_mongo

# Retrieve MongoDB credentials from environment variables
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = "review-db" 
COLLECTION_NAME = "products"

def find_by_url(client, db_name, collection_name, url):
    """Find a product by its URL in MongoDB."""
    db = client[db_name]
    collection = db[collection_name]
    return collection.find_one({"url": url})

def insert_if_not_exists(client, db_name, collection_name, document):
    """Checks if a document exists in the collection and inserts if not."""
    db = client[db_name]
    collection = db[collection_name]

    # Check if document exists based on the 'url'
    query = {"url": document["url"]}
    existing_doc = collection.find_one(query)

    if existing_doc:
        print(f"Document already exists: {existing_doc}")
    else:
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
        urls= [
        "https://kith.com/collections/kith-footwear/products/x2j162xf85500",
        "https://www.amazon.com/eos-Cashmere-Moisture-Lightweight-Non-Greasy/dp/B08KT2Z93D/?_encoding=UTF8&pd_rd_w=a3wu2&content-id=amzn1.sym.aeef70de-9e3e-4007-ae27-5dbb7b4a72f6&pf_rd_p=aeef70de-9e3e-4007-ae27-5dbb7b4a72f6&pf_rd_r=21NA7K6QEXX5X2F6N2KM&pd_rd_wg=l7cK3&pd_rd_r=903996a9-0eaa-4382-bfac-680c67cfe909&ref_=pd_hp_d_btf_crs_zg_bs_3760911",
        #Captcha"https://www.walmart.com/ip/Austin-Peanut-Butter-on-Cheese-Sandwich-Crackers-Single-Serve-Snack-Crackers-20-Count/1837462801?classType=REGULAR&athbdg=L1600&adsRedirect=true",
        #Timeout"https://www.meijer.com/shopping/product/sony-zx-series-stereo-headphones-black/2724286708.html",
        "https://us.shein.com/SHEIN-EZwear-Women-s-Hooded-Sweatshirt-With-Slogan-Print-And-Kangaroo-Pocket-FAITH-OVER-FEAR-PSALM-563-p-29621449.html?src_identifier=uf=usbingsearch09_cheaptrendyclothes02_20220804&src_module=ads&mallCode=1&pageListType=4&imgRatio=3-4",
        "https://www.gap.com/browse/product.do?pid=538469002&rrec=true&mlink=5001,1,home_gaphome2_rr_0&clink=1",
        "https://www.target.com/p/marvel-youth-spider-man-halloween-costume/-/A-90605950?preselect=90599841#lnk=sametab",
        "https://www.nike.com/t/ja-2-basketball-shoes-zNhj0Q/FD7328-500"
        ]
        for url in urls:
            prod_entry = get_product_and_description_from_url(url)
            document = get_questions_for_product(prod_entry)
            insert_if_not_exists(client, DB_NAME, COLLECTION_NAME, document)


if __name__ == "__main__":
    main()
