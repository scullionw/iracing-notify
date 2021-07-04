import redis
import json
from scraper import VIP


class Drivers:
    def __init__(self):
        self.redis_client = redis.Redis(host="redis-service", port=6379, db=0)
        self.notifications = []

    def get(self, name):
        value = self.redis_client.get(name)

        if value is None:
            return None

        return json.loads(value.decode("utf-8"))

    def set(self, name, info):
        self.redis_client.set(name, json.dumps(info))

    def update(self, driver_status: dict):
        for name, info in driver_status.items():
            previous_state = self.get(name)
            self.set(name, info)

            # Was NOT driving
            if previous_state is None:
                # Is now driving
                if info is not None:
                    self.add_to_notifications(name, notify_driving(name, info))
                # Is not driving
                else:
                    pass
            # Was driving
            else:
                # Is now driving
                if info is not None:
                    # Driving in different series
                    if info != previous_state:
                        self.add_to_notifications(name, notify_driving(name, info))
                    # Driving in same series
                    else:
                        pass
                # Is not driving
                else:
                    self.add_to_notifications(name, notify_stopped(name))

        self.send_notifications()

    def add_to_notifications(self, name, notification):
        if name in VIP["friends"]:
            self.notifications.append(notification)

    def send_notifications(self):
        message = "\n".join(self.notifications)
        self.notifications = []


def notify_driving(name, info):
    return (
        f"{name} is currently driving in {info['series_name']} - {info['event_type']}."
    )


def notify_stopped(name):
    return f"{name} has stopped driving."
