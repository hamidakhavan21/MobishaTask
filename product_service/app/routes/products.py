from fastapi import APIRouter, HTTPException
from app.services.product_service import fetch_and_store_products
import logging

logger = logging.getLogger("product_service")
router = APIRouter()

@router.get("/products/sync")
async def sync_products(username: str):
    try:
        result = await fetch_and_store_products(username)
        return {"message": "Products synchronized successfully.", "details": result}
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
