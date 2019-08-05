IRACING_LOGIN = 'https://members.iracing.com/membersite/Login'
IRACING_FRIENDS= "http://members.iracing.com/membersite/member/GetDriverStatus?friends=1&studied=1&blacklisted=1"
IRACING_HOME = "https://members.iracing.com/membersite/member/Home.do"

class iRacingClient:

    def __init__(self, credentials):
        self.session = requests.session()
        session.post(URL_IRACING_LOGIN, data=credentials)

    def friend_data(self):
        response = s.get(URL_API)
        data = response.json()

        friend_data = {}
        for driver in data['fsRacers']:
            name = clean_name(driver['name'])
            friend_data[name] = currently_driving(driver)

        return friend_data

    def session_data(self):
        session_data = {}
        for series, series_name in get_series(s).items():
            if ANY_SERIES or any([keyword.lower() in series_name.lower() for keyword in SERIES_KEYWORDS]):
                for subsession in get_subsessions(s, series):
                    for driver in get_drivers(s, subsession):
                        session_data[driver] = series_name

        return session_data

    def get_series(self):
        response = session.get(HOME_URL)
        text = response.text
        found = re.findall(r"var\sAvailSeries\s*=\s*extractJSON\('([\S\s]*?)'\);", text)
        data = json.loads(found[0])
        series = {}
        for entry in data:
            if entry['category'] == 2:
                series[entry['seasonid']] = clean_name(entry['seriesname'])
        return series

    def get_subsessions(self, series):
        response = session.get(f"https://members.iracing.com/membersite/member/GetOpenSessions?season={series}&invokedby=seriessessionspage")
        data = response.json()
        return [el['15'] for el in data['d']]

    def get_drivers(self, subsession):
        response = session.get(f"https://members.iracing.com/membersite/member/GetOpenSessionDrivers?subsessionid={subsession}&requestindex=0")
        data = response.json()
        return [clean_name(el['dn']) for el in data['rows']]