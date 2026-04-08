import os
#Influx config
INFLUXDB_TOKEN = 'jZ6wXym3jxyo_yxYjCo07ygyqUMFC9OEkCAQXjPNvWylyCQTpE3iqg2rF2DYoyA5XzYYgkSm5dsPmrgpOeq4qA=='#os.environ.get("INFLUXDB_TOKEN")
INFLUXDB_ORG = "MAgent-kafka"
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_BUCKET="MAC_Metrics"

#kafka config
KAFKA_BOOTSTRAP="kafka:9092"
KAFKA_TOPIC="metrics"
LOCAL_BOOTSTRAP="localhost:9092"

COLLECTION_INTERVAL = 10