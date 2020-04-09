import iracing_notify.config as config
import requests

NIMROD_URL = "https://www.nimrod-messenger.io/api/v1/message"


def notify(message):
    nimrod(message)


def nimrod(message):
    payload = {"api_key": config.api_key, "message": message}
    requests.post(NIMROD_URL, json=payload)
