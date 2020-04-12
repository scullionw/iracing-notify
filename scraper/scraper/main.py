import sys
from scraper.drivers import Drivers
from scraper.defaultdrivers import VIP
from iracing_web_api import iRacingClient, LoginFailed
import time
import requests
import json
from typing import Optional, Any, Dict, List
import os
import logging
import scraper.mock

SCRAPE_DELAY_MIN = 5
MIN_SECS = 60

API_URL = os.getenv("API_URL")
API_ENDPOINT_ADDR = f"{API_URL}/api/update"


def main():
    logging.info("Logging in..")

    try:
        username = os.getenv("IRACING_USERNAME")
        password = os.getenv("IRACING_PASSWORD")
        if not (username and password):
            logging.error("Must provide IRACING_USERNAME and IRACING_PASSWORD")
            sys.exit(1)

        iracing = iRacingClient(username, password)
    except LoginFailed:
        logging.warning("Login failed. Exiting. Wrong credentials or captcha required")
        sys.exit(1)
    else:
        logging.info("Logged in.")
        scrape(iracing)


def send_data(endpoint: str, data: List[dict]):
    logging.debug(f"POST to {endpoint}")
    try:
        requests.post(endpoint, json=data)
    except:
        logging.warning("API is down.")
    else:
        logging.debug("POST successful")


def adjust(data: dict) -> List[dict]:
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
        logging.info("Scraping..")
        driver_status = client.driver_status()
        logging.info("Finished scraping!")
        end = time.time()

        logging.info(f"Scraping took {end - start} seconds.")

        adjusted_data = adjust(driver_status)
        send_data(API_ENDPOINT_ADDR, adjusted_data)

        drivers = Drivers.load()
        drivers.update(driver_status)
        drivers.save()

        time.sleep(SCRAPE_DELAY_MIN * MIN_SECS)


if __name__ == "__main__":
    if "MOCKSCRAPE" in os.environ:
        logging.info("MOCKING!")
        sys.exit(scraper.mock.mock_scrape(API_ENDPOINT_ADDR))
    else:
        sys.exit(main())
