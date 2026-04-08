from kafka import KafkaProducer
import json
import psutil
import socket
import time
from .app_config import KAFKA_BOOTSTRAP, LOCAL_BOOTSTRAP, INFLUXDB_TOKEN

#create a kafka producer

def create_producer():
    print(INFLUXDB_TOKEN)
    return KafkaProducer(bootstrap_servers= ['localhost:9092'], value_serializer=lambda v: json.dumps(v).encode('utf-8'),api_version=(2, 3, 0))