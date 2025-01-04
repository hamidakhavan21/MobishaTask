from app.persist.token_repository import get_user_token
from app.persist.product_repository import update_product
import requests

async def fetch_and_store_products(username: str, page_size: int = 10, max_pages: int = 5):
    access_token = get_user_token(username)
    if not access_token:
        raise ValueError("token not found!")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    base_url = "https://seller.digikala.com/api/v2/variants"
    stored_count = 0

    for page in range(1, max_pages + 1):
        url = f"{base_url}?page={page}&size={page_size}&sort=product_variant_id&order=desc"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise ValueError(f"error while fetching data {response.status_code} - {response.text}")

        data = response.json()
        items = data.get("data", {}).get("items", [])
        if not items:
            break 

        for item in items:
            product_data = {
                "name": item.get("product_title"),
                "dkpc": item.get("product_variant_id"),
                "price": item.get("price_sale"),
                "stock": item.get("marketplace_seller_stock"),
                "status": "فعال" if item.get("active") else "غیرفعال",
                "created_at": item.get("created_at", {}).get("date"),
                "username": username
            }
            update_product(product_data)
            stored_count += 1

    return {"stored_count": stored_count}
