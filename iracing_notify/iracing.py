import requests
import re
import json
import urllib.parse
import multiprocessing as mp
from collections import ChainMap
from iracing_notify.notifications import notify

IRACING_LOGIN = 'https://members.iracing.com/membersite/Login'
IRACING_FRIENDS= "http://members.iracing.com/membersite/member/GetDriverStatus?friends=1&studied=1&blacklisted=1"
IRACING_HOME = "https://members.iracing.com/membersite/member/Home.do"
IRACING_PRACTICE_SUBSESSIONS = "https://members.iracing.com/membersite/member/GetOpenSessions?season={series_id}&invokedby=seriessessionspage"
IRACING_OPENSESSION_DRIVERS = "https://members.iracing.com/membersite/member/GetOpenSessionDrivers?subsessionid={subsession}&requestindex=0"
IRACING_SESSION_DRIVERS = "https://members.iracing.com/membersite/member/GetSessionDrivers?subsessionid={subsession}&requestindex=0"
IRACING_WATCH_SUBSESSIONS = "https://members.iracing.com/membersite/member/GetSpectatorSessions?type=road"

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
        series = self.series()

        # Practice sessions
        subsessions = {}
        for series_id, series_name in series.items():
            for subsession, event_type in self.practice_subsessions(series_id).items():
                subsessions[subsession] = {'series_id': series_id, 'series_name': series_name, 'event_type': event_type }
        
        for subsession, info in subsessions.items():
            for driver in self.open_session_drivers(subsession):
                session_data[driver] = info

        # Watch sessions
        subsessions = self.watch_subsessions(series)
        for subsession, info in subsessions.items():
            for driver in self.session_drivers(subsession):
                session_data[driver] = info

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

    def practice_subsessions(self, series_id):
        url = IRACING_PRACTICE_SUBSESSIONS.format(series_id=series_id)
        response = self.session.get(url)
        data = response.json()
        return { el['15']: 'Practice' for el in data['d'] }

    def watch_subsessions(self, series):
        response = self.session.get(IRACING_WATCH_SUBSESSIONS)
        data = response.json()
        subsessions = {}
        for el in data:
            subsession_id = el['subsessionid']
            series_id = el['seasonid']
            series_name = series[series_id]
            if el['evttype'] == 2:
                event_type = 'Practice'
            elif el['evttype'] == 5:
                event_type = 'Race'
            else:
                event_type = 'Other'

            subsessions[subsession_id] = {'series_id': series_id, 'series_name': series_name, 'event_type': event_type }

        return subsessions

    def open_session_drivers(self, subsession):
        url = IRACING_OPENSESSION_DRIVERS.format(subsession=subsession)
        response = self.session.get(url)
        data = response.json()
        return [self.clean(el['dn']) for el in data['rows']]

    def session_drivers(self, subsession):
        url = IRACING_SESSION_DRIVERS.format(subsession=subsession)
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
