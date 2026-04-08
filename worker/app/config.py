import os

#Influx config
INFLUXDB_TOKEN = 'VXEFHM5qElTvd6CgfZTILGMuDQPSuy9pZDxmotMWisuXcob37snnkAkDp3GbVx5EzrxEmpwdQEWr8rg8SSoKCg=='#os.environ.get("INFLUXDB_TOKEN")
INFLUXDB_ORG = "ORG_Metrics"
INFLUXDB_URL = "http://influxdb:8086"
INFLUXDB_BUCKET="BUCKET_mac_metrics"

#kafka config
KAFKA_BOOTSTRAP="kafka:29092"
KAFKA_TOPIC="metrics"

COLLECTION_INTERVAL = 10