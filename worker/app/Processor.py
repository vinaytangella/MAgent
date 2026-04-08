from influxdb_client import Point
from .config import INFLUXDB_BUCKET
import logging
import time


FLUSH_INTREVAL = 5
BATCH_SIZE = 10

class MetricProcessor:

    def __init__(self, write_api):
        self.batch = []
        self.time = time.time()
        self.BATCH_SIZE = 10
        self.FLUSH_INTERVAL = 5
        self.write_api = write_api
        self.bucket = bucket
        self.org = org
        self.last_flush = time.time()


  def process_mesage(self, data):
    try:
        logging.error(f'--process data---{data}----- {write_api}----')
        point = (Point('system_metrics').tag('host', data['hostname']).field('cpu', data['cpu']).field('memory', data['memory']))

        self.batch.append(point)

        if (len(self.batch) > self.BATCH_SIZE or (time.time() - self.last_flush) > self.FLUSH_INTERVAL):
            write_api.write(bucket=INFLUXDB_BUCKET, record=self.batch)
            logging.error(f'flushed {len(self.batch)} points')
            self.batch.clear()
            self.last_flush = time.time()
            
    except Exception as e:
        logging.error(f'An error has occured while trying to push data to influx - {e}')