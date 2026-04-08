from influxdb_client import InfluxDBClient
from .config import INFLUXDB_BUCKET, INFLUXDB_ORG, INFLUXDB_URL, INFLUXDB_TOKEN


def create_influx_client():
    client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
    return client, client.write_api()