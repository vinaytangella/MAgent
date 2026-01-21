import psutil
from pathlib import Path
from datetime import datetime
import time
import socket
import os
import urllib.request
import shutil
import tempfile
import ssl
import certifi
import tempfile

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
    print('bew file', new_file)
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
        "last_run":datetime.now(),
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
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        with open(log_dir, "a") as f:
            f.write(f"{datetime.now()} CPU: {cpu}%, Memory: {memory}%, Disk: {disk}%\n")
        agentHeartbeat()
    except Exception as e:
        recordAgentFailures()
        agentHeartbeat(status="error", error=str(e))

if __name__ == "__main__":
    try:
        latest = fetch_latest_version()
        if is_update_available(AGENT_VERSION, latest):
            if perform_update(latest):
                agentHeartbeat(status="updated", error=None)
                exit(0)  # let launchd restart us
    except Exception:
        pass  
    while True:
        collectMetrics()
        time.sleep(10)