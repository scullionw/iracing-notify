from iracing_notify.notifications import notify
from iracing_notify.config import VIP

class Driver:
    def __init__(self, name):
        self.name = name
        self.state = None

    def next_state(self, info):
        # Log
        if info is not None:
            notify(f"LOG: {self.name} is currently driving in {info['series_name']} - {info['event_type']}.")
            print(f"LOG: {self.name} is currently driving in {info['series_name']} - {info['event_type']}.")

        # Was NOT driving
        if self.state is None:
            # Is now driving
            if info is not None:
                self.set_driving(info)
            # Is not driving
            else:
                pass
        # Was driving
        else:
            # Is now driving
            if info is not None:
                # Driving in different series
                if info != self.state:
                    self.set_driving(info)
                # Driving in same series
                else:
                    pass
            # Is not driving
            else:
                self.set_not_driving()

    def set_driving(self, info):
        self.state = info
        for group, names in VIP.items():
            if self.name in names:
                notify(f"{self.name} is now driving in {info['series_name']} - {info['event_type']}.")

    def set_not_driving(self):
        self.state = None
        for group, names in VIP.items():
            if self.name in names:
                notify(f"{self.name} has stopped driving")
