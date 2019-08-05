import requests
import urllib.parse
import sys
import pickle
import config
import re
import json
from pathlib import Path
from twilio.rest import Client


NIMROD_URL = 'https://www.nimrod-messenger.io/api/v1/message'
VIP = ['Lando Norris', 'Max Verstappen']
SERIES_KEYWORDS = ['F3', 'IMSA', 'GT3', 'Barber']
ANY_SERIES = True

def main():
    drivers = Drivers.load()

    with requests.session() as s:
        
        friend_data = get_friend_data(s)
        session_data = get_session_data(s)
        filtered_data = { driver: session_data[driver] for driver in friend_data }


    drivers.update(friend_data, session_data)
    drivers.save()

def validate_scrape(friend_data, session_data):
    pass

## Scraping





## Notifications
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


## Helper functions
def currently_driving(driver_data):
    return 'sessionStatus' in driver_data and driver_data['sessionStatus'] != 'none'

def clean_name(driver):
    name = driver.replace('+', ' ')
    return urllib.parse.unquote(name)


## State machine
class Driver:
    def __init__(self, name):
        self.name = name
        self.state = 'Unknown'

    def next_state(self, input):
        if self.state == 'Driving':

        elif self.state == 'Not Driving':

        else:


## Driver processing and persistence
class Drivers:
    save_path = Path('data/drivers')

    def __init__(self):
        self.driver_map = {}

    def update(self, friend_data, session_data):
        for name in friend_data:
            self.driver_map[name] = {'is_driving': friend_data[name]}
            if name in session_data:
                self.driver_map[name]['series'] = session_data[name]
            

            if name in self.driver_map:
                was_driving = self.driver_map[name]
                if was_driving and is_driving:
                    pass
                elif was_driving and not is_driving:
                    notify(f"{name} has stopped driving.")
                elif not was_driving and is_driving:
                    notify(f"{name} is now driving.", name in VIP)
                else:
                    pass
                
    def process():

    def add_driver():

    def next_state():


    @classmethod
    def load(cls):
        if cls.save_path.exists():
            with cls.save_path.open(mode='rb') as f:
                return pickle.load(f)
        else:
            cls.save_path.parent.mkdir(exist_ok=True)
            return Drivers()
    
    def save(self):
        with self.save_path.open(mode='wb') as f:
            pickle.dump(self, f)


if __name__ == '__main__':
    sys.exit(main())
