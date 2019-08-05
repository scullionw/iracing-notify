import requests
import re
import json
import urllib.parse
from iracing_notify.notifications import notify
from iracing_notify.config import ANY_SERIES, SERIES_KEYWORDS

IRACING_LOGIN = 'https://members.iracing.com/membersite/Login'
IRACING_FRIENDS= "http://members.iracing.com/membersite/member/GetDriverStatus?friends=1&studied=1&blacklisted=1"
IRACING_HOME = "https://members.iracing.com/membersite/member/Home.do"
IRACING_SUBSESSIONS = "https://members.iracing.com/membersite/member/GetOpenSessions?season={series}&invokedby=seriessessionspage"
IRACING_SUBSESSION_DRIVERS = "https://members.iracing.com/membersite/member/GetOpenSessionDrivers?subsessionid={subsession}&requestindex=0"

class iRacingClient:

    def __init__(self, credentials):
        self.session = requests.session()
        self.session.post(IRACING_LOGIN, data=credentials)

    def driver_status(self):
        friend_data = self.friend_data()
        session_data = self.session_data()
        driver_status = {}
        for driver in friend_data:
            if driver in session_data:
                driver_status[driver] = session_data[driver]
            else:
                driver_status[driver] = None
        return driver_status
        
    def friend_data(self):
        response = self.session.get(IRACING_FRIENDS)
        data = response.json()

        friend_data = {}
        for driver in data['fsRacers']:
            name = self.clean(driver['name'])
            friend_data[name] = self.currently_driving(driver)

        return friend_data

    def session_data(self):
        session_data = {}
        for series, series_name in self.series().items():
            if ANY_SERIES or any([keyword.lower() in series_name.lower() for keyword in SERIES_KEYWORDS]):
                for subsession in self.subsessions(series):
                    for driver in self.drivers(subsession):
                        session_data[driver] = series_name

        return session_data

    def series(self):
        response = self.session.get(IRACING_HOME)
        text = response.text
        found = re.findall(r"var\sAvailSeries\s*=\s*extractJSON\('([\S\s]*?)'\);", text)
        data = json.loads(found[0])
        series = {}
        for entry in data:
            if entry['category'] == 2:
                series[entry['seasonid']] = self.clean(entry['seriesname'])
        return series

    def subsessions(self, series):
        url = IRACING_SUBSESSIONS.format(series=series)
        response = self.session.get(url)
        data = response.json()
        return [el['15'] for el in data['d']]

    def drivers(self, subsession):
        url = IRACING_SUBSESSION_DRIVERS.format(subsession=subsession)
        response = self.session.get(url)
        data = response.json()
        return [self.clean(el['dn']) for el in data['rows']]

    @staticmethod
    def validate_scrape(friend_data, session_data):
        for driver, driving in friend_data:
            if driving and driver not in session_data:
                notify("MISMATCH: ", driver)

    @staticmethod
    def currently_driving(driver_data):
        return 'sessionStatus' in driver_data and driver_data['sessionStatus'] != 'none'

    @staticmethod
    def clean(s):
        s = s.replace('+', ' ')
        return urllib.parse.unquote(s)
