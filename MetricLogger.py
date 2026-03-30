 import logging
 import time
 from formatter import JSONFormatter
 from CollectMetrics import CollectMetrics

 logger = logging.get_logger("mac_metrics")
 logger.setLevel(logging.INFO)

 handler = logging.FileHandler("/Users/$USER/Library/Logs/mac-metrics.log")

 handler.setFormatter(JSONFormatter())

 logger.addHandler(handler)