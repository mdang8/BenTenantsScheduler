import os
import json
from pprint import pprint
from CalendarSetup import CalendarSetup


def main():
    calendar_setup = CalendarSetup()
    calendar_setup.setup_new_driveway_schedule()


if __name__ == '__main__':
    main()
