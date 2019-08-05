from config import credentials
from iracing import iRacingClient
from drivers import Drivers
import sys

def main():
    iracing = iRacingClient(credentials)
    driver_status = iracing.driver_status()

    drivers = Drivers.load()
    drivers.update(driver_status)
    drivers.save()

if __name__ == '__main__':
    sys.exit(main())
