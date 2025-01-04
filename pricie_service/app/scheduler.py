from apscheduler.schedulers.background import BackgroundScheduler
from app.services.price_service import update_price

def schedule_price_updates():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        update_price,
        "interval",
        minutes=5,
        kwargs={"product_id": 57481108},  # شناسه محصول به صورت مثال
    )
    scheduler.start()
