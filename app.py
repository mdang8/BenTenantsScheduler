from dotenv import load_dotenv
from datetime import datetime
from src.flaskr import create_app
from src.lib.CalendarSetup import CalendarSetup

load_dotenv()


def main(setup=False, test=False):
    app = create_app()
    if setup:
        first_start_date = datetime(2019, 9, 8)
        first_end_date = datetime(2019, 9, 15)
        calendar_setup = CalendarSetup(first_start_date, first_end_date)
        calendar_setup.setup_new_schedule(calendar_name='BenTenants Driveway Schedule', test=test)
        calendar_setup.setup_new_schedule(calendar_name='BenTenants', test=test)

    return app


if __name__ == '__main__':
    flask_app = main(setup=False, test=False)
    flask_app.run(debug=True, host='0.0.0.0', port=5000)
