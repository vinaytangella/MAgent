import cotyledon
from .KafkaConsumer import create_consumer
from .InfluxClient import create_influx_client
from .Processor import MetricProcessor
import logging

class MetricsWorker(cotyledon.Service):
    def __init__(self, worker_id,**kwargs):
        super().__init__(worker_id, **kwargs)
        self.consumer = create_consumer()
        self.influx_client, self.write_api = create_influx_client()

    def run(self):
        processor = MetricsProcessor(self.write_api)
        for msg in self.consumer:
            try:
                logging.error(f'------{msg.value} ---- {self.write_api}---------')
                processor.process_message(msg.value)
            except Exception as e:
                logging.error(f"Error processing message: {e}")

                
