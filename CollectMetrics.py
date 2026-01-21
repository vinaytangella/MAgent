import psutil
from pathlib import Path
from datetime import datetime
import time
import socket
import os
import urllib.request
import shutil
import tempfile

cwd = str(Path.cwd())
log_dir = cwd+"/metrics.log"
hb_dir = cwd+"/heartbeat.log"
failure_count = cwd+"/failure_count.log"
HOSTNAME = socket.gethostname()
AGENT_NAME = "CollectMetrics"
AGENT_VERSION = "1.0.0" 

REPO_URL = "https://raw.githubusercontent.com/vinaytangella/MAagent/refs/heads/main/"
VERSION_URL = REPO_URL+"VERSION"
AGENT_URL = REPO_URL+"CollectMetrics.py"  


def fetchLatestVersion():
    print('VERSION_URL',VERSION_URL)
    with urllib.request.urlopen(VERSION_URL) as f:
        return f.read().decode("utf-8").strip()

def isUpdateAvailable():
    return AGENT_VERSION < fetchLatestVersion()


def agentHeartbeat(status="ok", error=None):
    heartbeat = {
        "agent":AGENT_NAME,
        "version":AGENT_VERSION,
        "status":status,
        "hostname":HOSTNAME,
        "last_run":datetime.now(),
        "error":error,
        "pid":os.getpid()
    }

    with(open(hb_dir, "a")) as f:
        f.write(f"{heartbeat}\n")

def recordAgentFailures():
    count = 0
    if failure_count.exists():
        with open(failure_count, "r") as f:
            count = int(f.read())
    count += 1
    with open(failure_count, "w") as f:
        f.write(str(count))

def collectMetrics():
    try:
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        with open(log_dir, "a") as f:
            f.write(f"{datetime.now()} CPU: {cpu}%, Memory: {memory}%, Disk: {disk}%\n")
        agent_heartbeat()
    except Exception as e:
        recordAgentFailures()
        agent_heartbeat(status="error", error=str(e))

if __name__ == "__main__":
    while True:
        isUpdateAvailable()
        # collectMetrics()
        time.sleep(10)