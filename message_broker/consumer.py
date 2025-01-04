from kafka import KafkaConsumer
import json
from persist.log_repository import save_log
from config.settings import KAFKA_BROKER_URL

consumer = KafkaConsumer(
    "price_update_logs",
    bootstrap_servers=KAFKA_BROKER_URL,
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    log_entry = message.value
    save_log(log_entry)
