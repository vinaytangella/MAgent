import time
from .MetricCollector import collect_metrics
from .KafkaProducer import create_producer
from .app_config import KAFKA_TOPIC, COLLECTION_INTERVAL


def run():
    producer = create_producer()

    while True:
        data = collect_metrics()
        producer.send(KAFKA_TOPIC, data)
        print('data-sent', data)
        time.sleep(COLLECTION_INTERVAL)