import aiohttp
import math
from datetime import datetime
from app.persist.price_repository import log_price_change, get_product_price, get_product_Id
from app.persist.token_repository import get_user_token  


API_URL = "https://seller.digikala.com/api/v2/variants/{product_id}"
PERCENTAGE_INCREASE = 10  

async def update_price(username: str):
    product_id = get_product_Id(username)
    if product_id is None:
        raise ValueError("Username not found!")

    current_price = get_product_price(product_id)
    if current_price is None:
        raise ValueError("Product ID not found!")

    new_price = math.floor(current_price * (1 + (PERCENTAGE_INCREASE / 100)) / 100) * 100
    payload = {
        "id": product_id,
        "selling_price": new_price,
        "lead_time": 2,
        "shipping_type": "digikala",
    }

    access_token = get_user_token(username)
    if not access_token:
        raise ValueError("Access token not found for the user!")

    headers = {
        "Authorization": f"Bearer {access_token}",  
        "Content-Type": "application/json",
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.put(API_URL.format(product_id=product_id), json=payload, headers=headers) as response:
                response_data = await response.json()
                
                log_entry = {
                    "product_id": product_id,
                    "old_price": current_price,
                    "new_price": new_price,
                    "timestamp": datetime.utcnow(),
                    "status": "success" if response.status == 200 else "failed",
                    "api_response": response_data,
                }
                log_price_change(log_entry)
                
                if response.status != 200:
                    raise Exception(f"API Error: {response.status} - {response_data}")
                
                return log_entry
        except Exception as e:
            log_entry = {
                "product_id": product_id,
                "old_price": current_price,
                "new_price": new_price,
                "timestamp": datetime.utcnow(),
                "status": "failed",
                "api_response": str(e),
            }
            log_price_change(log_entry)
            raise e
