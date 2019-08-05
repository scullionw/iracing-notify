from notifications import notify
from config import VIP

class Driver:
    def __init__(self, name):
        self.name = name
        self.state = None

    def next_state(self, current_series):
        # Was NOT driving
        if self.state is None:
            # Is now driving
            if current_series is not None:
                self.set_driving(current_series)
            # Is not driving
            else:
                pass
        # Was driving
        else:
            # Is now driving
            if current_series is not None:
                # Driving in different series
                if current_series != self.state:
                    self.set_driving(current_series)
                # Driving in same series
                else:
                    pass
            # Is not driving
            else:
                self.set_not_driving()

    def set_driving(self, series):
        self.state = series
        notify(f"{self.name} is now driving in {series}.", self.name in VIP)

    def set_not_driving(self):
        self.state = None
        notify(f"{self.name} has stopped driving", self.name in VIP)
