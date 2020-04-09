import sys
from scraper.config import credentials
from scraper.drivers import Drivers
from scraper.config import VIP
from iracing_web_api import iRacingClient, LoginFailed
import time
import requests
import json
from typing import Optional, Any, Dict, List

SCRAPE_DELAY_MIN = 5
MIN_SECS = 60

API_ENDPOINT_ADDR = "http://api:8000/api/update"

MOCK_SCRAPE = DRIVER_STATUS_MOCK = [
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


def main():
    print("Logging in.")

    try:
        iracing = iRacingClient(credentials["username"], credentials["password"])
    except LoginFailed:
        print("Login failed. Exiting.")
    else:
        print("Logged in.")
        scrape(iracing)


def send_data(data: Dict):
    requests.post(API_ENDPOINT_ADDR, json=adjust(data))


def adjust(data: Dict) -> List[Dict[str, Any]]:
    adjusted = []
    for name, info in data.items():
        adjusted.append(
            {
                "name": name,
                "category": category(name),
                "driving": info
                and {
                    "track": "Unknown",
                    "car": "Unknown",
                    "series": info["series_name"],
                    "session_type": info["event_type"],
                },
            }
        )

    return adjusted


def category(name: str) -> str:
    for cat, names in VIP.items():
        if name in names:
            return cat

    return "Other"


def scrape(client: iRacingClient):
    while True:
        start = time.time()
        print("Scraping..")
        driver_status = client.driver_status()
        print("Finished scraping!")
        end = time.time()

        print(f"Scraping took {end - start} seconds.")

        send_data(driver_status)

        drivers = Drivers.load()
        drivers.update(driver_status)
        drivers.save()

        time.sleep(SCRAPE_DELAY_MIN * MIN_SECS)


def mock_scrape():
    while True:
        print(f"POST to {API_ENDPOINT_ADDR}")
        try:
            requests.post(API_ENDPOINT_ADDR, json=MOCK_SCRAPE)
        except:
            print("API IS DOWN.")
        else:
            print("Post successful.")
        time.sleep(10)


if __name__ == "__main__":
    # sys.exit(main())
    mock_scrape()
