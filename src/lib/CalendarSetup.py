import os
import json
from time import sleep
from datetime import timedelta
from pprint import pprint
from src.lib.Authorize import Authorize
from src.lib.Calendar import Calendar


class CalendarSetup:
    # beginning and end dates to start frequency counting at
    FIRST_START_DATE = None
    FIRST_END_DATE = None
    CALENDARS_INFO_FILE = os.path.abspath('src/configs/calendars.json')
    TENANTS_INFO_FILE = os.path.abspath('src/configs/tenants_info.json')
    available_calendars = None
    tenants_data = None
    calendar = None
    chores = ['Trash/Recycling', 'Dishwasher', 'Kitchen Counter-tops', 'Kitchen Floor', 'Stove-tops']

    def __init__(self, first_start_date, first_end_date):
        with open(self.CALENDARS_INFO_FILE) as f:
            self.available_calendars = json.load(f)
            f.close()
        with open(self.TENANTS_INFO_FILE) as f:
            self.tenants_data = json.load(f)
            f.close()
        self.FIRST_START_DATE = first_start_date
        self.FIRST_END_DATE = first_end_date
        auth = Authorize(['write'])
        creds = auth.create_token()
        self.calendar = Calendar(creds, '')

    def setup_new_schedule(self, calendar_name, test=False):
        calendar_id = self.find_calendar_id(calendar_name) if not test else self.find_calendar_id('Test')
        self.calendar.set_calendar_id(calendar_id)
        self.calendar.clear_all_events()
        events = self.create_chore_schedule() if calendar_name == 'BenTenants' else self.create_driveway_schedule()
        for event in events:
            created_event = self.calendar.create_event(event)
            pprint(created_event)
            sleep(0.5)

    # Finds the ID of the calendar associated with the given name.
    def find_calendar_id(self, name):
        calendar_id = next(filter(lambda x: x['name'] == name, self.available_calendars))['id']
        return calendar_id

    # Creates an event object to be used in an calendar event creation request.
    def build_driveway_event(self, tenant_pair, start_date, end_date, color_id):
        date_format = '%Y-%m-%d'
        # RRULE string for every 3 weeks frequency until 09/01/2020
        rrule = 'FREQ=WEEKLY;BYDAY=MO;INTERVAL=5;UNTIL=20200901T040000Z'
        event = {
            'summary': f'[ {tenant_pair[0]} + {tenant_pair[1]} ] - out on the streetz',
            'start': {
                'date': start_date.strftime(date_format),
                'timeZone': 'America/New_York'
            },
            'end': {
                'date': end_date.strftime(date_format),
                'timeZone': 'America/New_York'
            },
            'recurrence': [
                'RRULE:{}'.format(rrule)
            ],
            'attendees': [
                { 'email': self.tenants_data[tenant_pair[0]]['email'] },
                { 'email': self.tenants_data[tenant_pair[1]]['email'] }
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    { 'method': 'email', 'minutes': 24 * 60 }
                ]
            },
            'colorId': color_id
        }
        return event

    def build_chore_event(self, tenant_name, chore, start_date, end_date, color_id):
        date_format = '%Y-%m-%d'
        # RRULE string for every 3 weeks frequency until 09/01/2020
        rrule = 'FREQ=WEEKLY;BYDAY=SU;INTERVAL=5;UNTIL=20200901T040000Z'
        event = {
            'summary': f'[ {tenant_name.upper()} ] - {chore}',
            'start': {
                'date': start_date.strftime(date_format),
                'timeZone': 'America/New_York'
            },
            'end': {
                'date': end_date.strftime(date_format),
                'timeZone': 'America/New_York'
            },
            'recurrence': [
                f'RRULE:{rrule}'
            ],
            'attendees': [
                { 'email': self.tenants_data[tenant_name]['email'] }
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    { 'method': 'email', 'minutes': 12 * 60 }
                ]
            },
            'colorId': color_id
        }
        return event

    def create_driveway_schedule(self):
        tenant_pairs = self.shifting_pairings()
        events = []
        start_date = self.FIRST_START_DATE
        end_date = self.FIRST_END_DATE
        color_id = 1
        for tenant_pair in tenant_pairs:
            events.append(self.build_driveway_event(tenant_pair, start_date, end_date, str(color_id)))
            start_date = start_date + timedelta(days=7)
            end_date = start_date + timedelta(days=7)
            color_id = (color_id + 1) % 11
        return events

    def create_chore_schedule(self):
        events = []
        color_id = 1
        # the index to start accessing the chores list from
        chore_start_index = 0
        # loops through each tenant and creates events for each chore
        for tenant in self.tenants_data:
            start_date = self.FIRST_START_DATE
            end_date = self.FIRST_END_DATE
            # loops through the number of chores
            for i in range(len(self.chores)):
                # (chore_start_index + i) mod (length of chores) calculates the correct index of the chore to access
                # since we're looping through each tenant and need to avoid assigning duplicate chores to different
                # tenants
                events.append(self.build_chore_event(tenant, self.chores[(chore_start_index + i) % len(self.chores)], start_date, end_date, color_id))
                # increments the start/end dates for the next chore assigned to this tenant
                start_date = start_date + timedelta(days=7)
                end_date = start_date + timedelta(days=7)
            # for the next tenant we need to increment the chore start index so we can access the next chore in the
            # cycle
            chore_start_index = (chore_start_index + 1) % len(self.chores)
            # there are 11 available colors and we cycle the ID so each tenant is assigned the same color for all of
            # their events
            color_id = (color_id + 1) % 11
        return events

    def renew_events_end_date(self, calendar_name, end_year='2020'):
        calendar_id = self.find_calendar_id(calendar_name)
        self.calendar.set_calendar_id(calendar_id)
        self.calendar.renew_all_events(end_year)

    # Transforms the tenants info object to have the parking order number as the keys for better
    # retrieval.
    def order_number_as_keys(self):
        ordered_tenants_info = {}
        for tenant in self.tenants_data:
            ordered_tenants_info[self.tenants_data[tenant]['parking_order']] = tenant
        return ordered_tenants_info

    # Determines all of the possible pairings of tenants out on the streets. Each tenant has a
    # a pre-assigned order number between 0 and 4 (5 tenants total). Pairings are determined by
    # starting at the first 0th-1th index pair and shifting the indices up one at a time until
    # reaching the 0th-1th index again. Ex: [0, 1], [1, 2], [2, 3], ...
    def shifting_pairings(self):
        # use tenants info object with order numbers as keys for more efficient access
        ordered_tenants_info = self.order_number_as_keys()
        pairings = []
        p1 = 0
        p2 = 1
        while True:
            tenant_name_1 = ordered_tenants_info[str(p1)]
            tenant_name_2 = ordered_tenants_info[str(p2)]
            pairings.append([tenant_name_1, tenant_name_2])
            p1 = (p1 + 1) % 5
            p2 = (p2 + 1) % 5
            if p1 == 0 and p2 == 1:
                break
        return pairings
