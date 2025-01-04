from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client.digikala

def update_product(product_data: dict):
    db.products.update_one(
        {"dkpc": product_data["dkpc"]},  
        {"$set": product_data},
        upsert=True,  
    )
