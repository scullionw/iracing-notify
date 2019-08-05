import iracing_notify.config as config
import requests
from twilio.rest import Client

NIMROD_URL = 'https://www.nimrod-messenger.io/api/v1/message'

def notify(message, important=False):
    print(message)
    nimrod(message)
    if important:
        twilio(message)
    
def twilio(message):
    account_sid = config.account_sid
    auth_token = config.auth_token
    client = Client(account_sid, auth_token)

    message = client.messages \
            .create(
                body=message,
                from_=config.from_,
                to=config.to
            )

def nimrod(message):
    payload = { 'api_key' : config.api_key, 'message' : message }
    requests.post(NIMROD_URL, json=payload)