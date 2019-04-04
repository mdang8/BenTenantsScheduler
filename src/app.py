import os, sys
import json
from dotenv import load_dotenv
from src.flaskr import create_app
from src.lib.CalendarSetup import CalendarSetup

load_dotenv()


def main(setup=False):
    app = create_app()
    if setup:
        calendar_setup = CalendarSetup()
        calendar_setup.setup_new_driveway_schedule()
    return app


if __name__ == '__main__':
    main()
