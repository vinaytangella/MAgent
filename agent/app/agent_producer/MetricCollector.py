import os
import psutil
import time
import socket


HOST = socket.gethostname()

def collect_metrics():
    return {
        "hostname": HOST,
        "cpu":psutil.cpu_percent(),
        "memory":psutil.virtual_memory().percent
    }
