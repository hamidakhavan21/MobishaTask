from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client.digikala

def log_price_change(log_entry: dict):
    db.price_logs.insert_one(log_entry)

def get_product_price(product_id: int):
    product = db.products.find_one({"dkpc": product_id})
    if product:
        return product.get("price")
    return None


def get_product_Id(username: str):
    product_Id = db.products.find_one(
        {"username": username}, 
        sort=[("created_at", -1)] 
    )
    if product_Id:
        return product_Id.get("dkpc")
    return None