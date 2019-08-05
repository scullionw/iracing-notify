import requests
import urllib.parse
import sys
import pickle
import config
from pathlib import Path
from twilio.rest import Client

URL_IRACING_LOGIN = 'https://members.iracing.com/membersite/Login'
URL_API = "http://members.iracing.com/membersite/member/GetDriverStatus?friends=1&studied=1&blacklisted=1"
NIMROD_URL = 'https://www.nimrod-messenger.io/api/v1/message'
VIP = ['Lando Norris', 'Max Verstappen']

def main():
    drivers = Drivers.load()

    with requests.session() as s:
        # Login
        s.post(URL_IRACING_LOGIN, data=config.credentials)
        # Driver status API request
        response = s.get(URL_API)

    data = response.json()
    drivers.update(data)
    drivers.save()

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

def currently_driving(driver_data):
    return 'sessionStatus' in driver_data and driver_data['sessionStatus'] != 'none'

def driver_name(driver):
    name = driver['name'].replace('+', ' ')
    return urllib.parse.unquote(name)

class Drivers:
    save_path = Path('data/drivers')

    def __init__(self):
        ## Map<str, bool>
        self.driver_map = {}
    
    def add(self, driver, state):
        self.driver_map[driver] = state

    def update(self, data):
        for driver in data['fsRacers']:

            name = driver_name(driver)
            is_driving = currently_driving(driver)

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
                
            self.driver_map[name] = is_driving


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

