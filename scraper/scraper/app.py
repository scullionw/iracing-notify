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
from spontit import SpontitResource

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
        resource = SpontitResource(
            "william_scullion7383",
            "JAC7U2XK9VD9UQ44W30B73QZFVBIW88B5T82DNMB6XF7B8EQGOFR19COSWL1Z1NHVS7MMBBRAPCYLNHX0JM9GLGHLJH7HUCVKGR8",
        )
        drivers = Drivers(resource)
        scrape(iracing, drivers)


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
                    "subsession": info["subsession"]
                },
            }
        )

    return adjusted


def category(name: str) -> str:
    for cat, names in VIP.items():
        if name in names:
            return cat

    return "Other"


def scrape(client: iRacingClient, drivers):
    while True:
        start = time.time()
        logging.info("Scraping..")

        try:
            driver_status = client.driver_status()
        except json.decoder.JSONDecodeError:
            logging.warning("JSON decoding error. Maybe iRacing is down?")
        else:
            adjusted_data = adjust(driver_status)
            send_data(API_ENDPOINT_ADDR, adjusted_data)

            drivers.update(driver_status)

            log_status(driver_status)
        finally:
            logging.info("Finished scraping!")

            end = time.time()
            logging.info(f"Scraping took {end - start} seconds.")

            time.sleep(SCRAPE_DELAY_MIN * MIN_SECS)


def log_status(driver_status):
    logging.info("--- Scrape results ---")
    for name, info in driver_status.items():
        if info is not None:
            logging.info(
                f"{name} is currently driving in {info['series_name']} - {info['event_type']}."
            )


if __name__ == "__main__":
    sys.exit(main())
