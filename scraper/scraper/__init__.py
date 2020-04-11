__version__ = "0.1.0"

import logging
import os

logging.basicConfig(
    format="%(levelname)s:     %(message)s", level=os.environ.get("LOGLEVEL", "INFO"),
)
