import os
import json
from pprint import pprint
from Authorize import Authorize
from Calendar import Calendar


# beginning and end dates to start frequency counting at
START_DATE = '2019-03-11'
END_DATE = '2019-03-18'

tenants_info_file = os.path.abspath('configs/tenants_info.json')
with open(tenants_info_file) as f:
    TENANTS_DATA = json.load(f)
    f.close()


# Creates an event object to be used in an calendar event creation request.
def build_driveway_event(tenant_name, tenant_email):
    # RRULE string for every 3 weeks frequency until 09/01/2019
    rrule = 'FREQ=WEEKLY;BYDAY=MO;INTERVAL=3;UNTIL=20190901T040000Z'
    event = {
        'summary': '[ {} ] - out on the streetz'.format(tenant_name),
        'start': {
            'date': START_DATE,
            'timeZone': 'America/New_York'
        },
        'end': {
            'date': END_DATE,
            'timeZone': 'America/New_York'
        },
        'recurrence': [
            'RRULE:{}'.format(rrule)
        ],
        'attendees': [
            # { 'email': tenant_email }
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                { 'method': 'email', 'minutes': 24 * 60 }
            ]
        }
    }

    return event


def create_driveway_schedule():
    events = []
    for tenant in TENANTS_DATA:
        events.append(build_driveway_event(tenant, TENANTS_DATA[tenant]['email']))

    return events


def pairs_permutations(tenants_info):
    permutations = []
    p1 = -1
    p2 = 0
    while p1 != 0 and p2 != 1:
        p1 = (p1 + 1) % 5
        p2 = (p2 + 1) % 5
        permutations.append([p1, p2])
    return


def main():
    calendars_info_file = os.path.abspath('configs/calendars.json')
    with open(calendars_info_file) as f:
        available_calendars = json.load(f)
        f.close()
    driveway_schedule = next(filter(
            lambda x: x.name == 'BenTenants Driveway Schedule', available_calendars))

    scopes = ['write']
    auth = Authorize(scopes)
    creds = auth.create_token()
    calendar = Calendar(creds, driveway_schedule.id)
    # calendars = calendar.get_available_calendars()
    # pprint(calendars)
    events = create_driveway_schedule()
    for event in events:
        created_event = calendar.create_event(event)
        pprint(created_event)


if __name__ == '__main__':
    main()
