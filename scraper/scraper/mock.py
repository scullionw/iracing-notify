import logging
import time
from scraper.main import send_data
from typing import List

MOCK_SCRAPE_DELAY_SECS = 5

MOCK_SCRAPE: List[dict] = [
    {
        "name": "Max Verstappen FROM SCRAPER",
        "category": "F1",
        "driving": {
            "track": "Gilles-Villeneuve",
            "car": "Dallara F3",
            "series": "F3 Championship",
            "session_type": "Practice",
        },
    },
    {
        "name": "Charles Leclerc",
        "category": "F1",
        "driving": {
            "track": "Gilles-Villeneuve",
            "car": "Dallara F3",
            "series": "F3 Championship",
            "session_type": "Practice",
        },
    },
    {"name": "Lando Norris", "category": "F1", "driving": None},
    {"name": "Suellio Almeida", "category": "Sim", "driving": None},
]


def mock_scrape(endpoint: str):
    while True:
        send_data(endpoint, MOCK_SCRAPE)
        time.sleep(MOCK_SCRAPE_DELAY_SECS)
