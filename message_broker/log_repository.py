from config.database import db

def save_log(log_entry):
    db.price_change_logs.insert_one(log_entry)
