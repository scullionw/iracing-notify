import sys
from iracing_notify.config import credentials
from iracing_notify.drivers import Drivers
from iracing_web_api.iracing_web_api import iRacingClient


def main():
    print("Fetching..")
    iracing = iRacingClient(credentials["username"], credentials["password"])
    driver_status = iracing.driver_status()

    print(driver_status)

    drivers = Drivers.load()
    drivers.update(driver_status)
    drivers.save()
    print("Done.")

if __name__ == '__main__':
    sys.exit(main())
