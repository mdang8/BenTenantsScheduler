import os
import json
from pprint import pprint
from CalendarSetup import CalendarSetup
from MessagesClient import MessagesClient


def main():
    calendar_setup = CalendarSetup()
    messages_client = MessagesClient()
    # calendar_setup.setup_new_driveway_schedule()


if __name__ == '__main__':
    main()
