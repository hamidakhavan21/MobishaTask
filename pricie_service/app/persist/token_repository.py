from pymongo import MongoClient
from app.config.settings import DATABASE_NAME,DATABASE_URL

client = MongoClient(DATABASE_URL)
db = client[DATABASE_NAME]

def get_user_token(username: str) -> str:
    user_data = db.tokens.find_one({"username": username})
    if not user_data:
        raise ValueError("token not found!")
    return user_data.get("access_token")