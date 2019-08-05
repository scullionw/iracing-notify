import sys
from iracing_notify.config import credentials
from iracing_notify.iracing import iRacingClient
from iracing_notify.drivers import Drivers


def main():
    iracing = iRacingClient(credentials)
    driver_status = iracing.driver_status()

    drivers = Drivers.load()
    drivers.update(driver_status)
    drivers.save()

if __name__ == '__main__':
    sys.exit(main())
