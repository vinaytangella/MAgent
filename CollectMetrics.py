import psutil
import platform
from pathlib import Path
from datetime import datetime, timezone
import time
import socket
import os
import urllib.request
import shutil
import tempfile
import ssl
import certifi
import tempfile
import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS

import logging

cwd = str(Path.cwd())
log_dir = cwd+"/metrics.log"
hb_dir = cwd+"/heartbeat.log"
failure_count = cwd+"/failure_count.log"
HOSTNAME = socket.gethostname()
AGENT_NAME = "CollectMetrics"
AGENT_VERSION = "1.0.0" 
AGENT_PATH = cwd+"/CollectMetrics.py"

REPO_URL = "https://raw.githubusercontent.com/vinaytangella/MAgent/refs/heads/main/"
VERSION_URL = REPO_URL+"VERSION"
AGENT_URL = REPO_URL+"CollectMetrics.py"  

influx_token = os.environ.get("INFLUXDB_TOKEN")
influx_org = "MAgent"
influx_url = "http://localhost:8086"



def fetchLatestVersion():
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    with urllib.request.urlopen(VERSION_URL,context=ssl_context) as f:
        return f.read().decode("utf-8").strip()

def isUpdateAvailable():
    def parse(v):
        return tuple(map(int, v.split(".")))
    return parse(AGENT_VERSION) > parse(fetchLatestVersion())


def download_new_agent():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        with urllib.request.urlopen(AGENT_URL, timeout=10) as resp:
            tmp.write(resp.read())
        return tmp.name

def replace_agent(new_file):
    backup = AGENT_PATH + ".bak"
    shutil.copy2(AGENT_PATH, backup)
    shutil.move(new_file, AGENT_PATH)

def perform_update(latest_version):
    try:
        tmp = download_new_agent()
        replace_agent(tmp)
        return True
    except Exception as e:
        agentHeartbeat(status="update_failed", error=str(e))
        return False

def agentHeartbeat(status="ok", error=None):
    heartbeat = {
        "agent":AGENT_NAME,
        "version":AGENT_VERSION,
        "status":status,
        "hostname":HOSTNAME,
        "last_run":datetime.now(timezone.utc),
        "error":error,
        "pid":os.getpid()
    }

    with(open(hb_dir, "a")) as f:
        f.write(f"{heartbeat}\n")

def recordAgentFailures():
    count = 0
    failure_count_path = Path(failure_count)
    if failure_count_path.exists():
        with open(failure_count, "r") as f:
            count = int(f.read())
    count += 1
    with open(failure_count, "w") as f:
        f.write(str(count))

def collectMetrics():
    try:
        metrics = {
            "timestamp": datetime.now(timezone.utc),

            "system": {
                "hostname": socket.gethostname(),
                "os": platform.system(),
                "os_version": platform.version(),
                "architecture": platform.machine()
            },

            "cpu": {
                "percent": psutil.cpu_percent(interval=1),
                "count": psutil.cpu_count(logical=True)
            },

            "memory": {
                "total": psutil.virtual_memory().total,
                "used": psutil.virtual_memory().used,
                "percent": psutil.virtual_memory().percent
            },

            "disk": {
                "disk_total": psutil.disk_usage('/').total,
                "disk_used": psutil.disk_usage('/').used,
                "disk_percent": psutil.disk_usage('/').percent
            },

            "network": {
                "bytes_sent": psutil.net_io_counters().bytes_sent,
                "bytes_recv": psutil.net_io_counters().bytes_recv
            }
        }

        return metrics
    except Exception as e:
        recordAgentFailures()
        agentHeartbeat(status="error", error=str(e))
        return {}

if __name__ == "__main__":
    try:
        # latest = fetch_latest_version()
        write_client = influxdb_client.InfluxDBClient(url=influx_url, token=influx_token, org=influx_org)
        logging.error(write_client)
        write_api = write_client.write_api(write_options=WriteOptions(batch_size=100,flush_interval=5000,retry_interval=2000,max_retries=5))
        
        # if is_update_available(AGENT_VERSION, latest):
        #     if perform_update(latest):
        #         agentHeartbeat(status="updated", error=None)
        #         exit(0)  # let launchd restart us
    except Exception as e:
        logging.error(f'This is exception: {e}')
        pass  
    while True:
        metrics = collectMetrics()
        point = (
            Point("system_metrics")
            .tag("host", socket.gethostname())
            .field("cpu_percent", metrics.get('cpu')['percent'])
            .field("cpu_count", metrics.get('cpu')['count'])
            .field('memory_used', metrics.get('memory')['used'])
            .field('memory_percent', metrics.get('memory')['percent'])
            .field('memory_total', metrics.get('memory')['total']))
        write_api.write(bucket="mac_metrics", record=point)
        time.sleep(10)