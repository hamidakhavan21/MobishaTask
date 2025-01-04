from fastapi import APIRouter, HTTPException
from app.services.price_service import update_price

router = APIRouter()

@router.put("/prices/update")
async def change_product_price(username: str):
    try:
        result = await update_price(username)
        return {"message": "Price updated successfully.", "details": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
