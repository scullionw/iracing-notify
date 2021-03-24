from scraper.driver import Driver
import redis
import json
import logging


class Drivers:
    def __init__(self, resource):
        self.redis_client = redis.Redis(host="redis-service", port=6379, db=0)
        self.resource = resource

    def get(self, name):
        value = self.redis_client.get(name)

        if value is None:
            return None

        return json.loads(value.decode("utf-8"))

    def set(self, name, info):
        self.redis_client.set(name, json.dumps(info))

    def update(self, driver_status: dict):
        notifications = []
        for name, info in driver_status.items():
            previous_state = self.get(name)
            self.set(name, info)

            # Was NOT driving
            if previous_state is None:
                # Is now driving
                if info is not None:
                    notifications.append(notify_driving(name, info))
                # Is not driving
                else:
                    pass
            # Was driving
            else:
                # Is now driving
                if info is not None:
                    # Driving in different series
                    if info != previous_state:
                        notifications.append(notify_driving(name, info))
                    # Driving in same series
                    else:
                        pass
                # Is not driving
                else:
                    notifications.append(notify_stopped(name))

        message = "\n".join(notifications)
        self.resource.push(message)


def notify_driving(name, info):
    return (
        f"{name} is currently driving in {info['series_name']} - {info['event_type']}."
    )


def notify_stopped(name):
    return f"{name} has stopped driving."
