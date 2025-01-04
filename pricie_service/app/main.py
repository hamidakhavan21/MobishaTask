from fastapi import FastAPI
from app.routes import price
from app.scheduler import schedule_price_updates
import uvicorn

app = FastAPI()
app.include_router(price.router, prefix="/api/v1")

if __name__ == "__main__":
    schedule_price_updates()
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
