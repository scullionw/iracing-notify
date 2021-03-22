__version__ = "0.1.0"

import logging
import os

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=os.environ.get("LOGLEVEL", logging.INFO),
    datefmt='%Y-%m-%d %H:%M:%S %Z'
)