from scraper.defaultdrivers import VIP
import logging
import os
from typing import Optional


class Driver:
    def __init__(self, name: str):
        self.name: str = name
        self.state: Optional[dict] = None

    def next_state(self, info: Optional[dict]):
        # Log
        if info is not None:
            logging.info(
                f"{self.name} is currently driving in {info['series_name']} - {info['event_type']}."
            )

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

    def set_driving(self, info: Optional[dict]):
        self.state = info

    def set_not_driving(self):
        self.state = None
