import requests
import json
import urllib.parse
import sys
from config import credentials, api_key

URL_IRACING_LOGIN = 'https://members.iracing.com/membersite/Login'
URL_API = "http://members.iracing.com/membersite/member/GetDriverStatus?friends=1&studied=1&blacklisted=1"
NIMROD_URL = 'https://www.nimrod-messenger.io/api/v1/message'

def main():
    print("Running..")

    with requests.session() as s:
        # Login
        s.post(URL_IRACING_LOGIN, data=credentials)
        # Data request
        response = s.get(URL_API)

    data = json.loads(response.text)

    for driver in data['fsRacers']:
        if 'sessionStatus' in driver:
            if driver['sessionStatus'] != 'none':
                name = driver['name'].replace('+', ' ')
                name = urllib.parse.unquote(name)
                message = f"{name} is currently driving."
                print(message)
                notify(message)

    print("Done.")

def notify(message):
    payload = { 'api_key' : api_key, 'message' : message }
    requests.post(NIMROD_URL, json=payload)

if __name__ == '__main__':
    sys.exit(main())

