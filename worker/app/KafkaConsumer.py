from kafka import KafkaConsumer
from .config import KAFKA_TOPIC, KAFKA_BOOTSTRAP
import json

def create_consumer():
    return KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=KAFKA_BOOTSTRAP, value_deserializer=lambda v: json.loads(v.decode('utf-8')), auto_offset_reset="earliest",enable_auto_commit=True,group_id="metrics_group_latest_april8", session_timeout_ms=60000,heartbeat_interval_ms=20000,request_timeout_ms=61000,api_version=(2, 3, 0))