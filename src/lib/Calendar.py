from os import path
from json import load
from datetime import datetime, timedelta, timezone
from time import sleep
from googleapiclient.discovery import build
from src.lib.Authorize import Authorize


creds = Authorize(['write']).create_token()
service = build('calendar', 'v3', credentials=creds)
CALENDARS_INFO_FILE = path.abspath('configs/calendars.json')
with open(CALENDARS_INFO_FILE) as f:
    available_calendars = load(f)
    f.close()


# Finds the ID of the calendar associated with the given name.
def find_calendar_id(calendar_name):
    return next(filter(lambda x: x['name'] == calendar_name, available_calendars))['id']


# Makes a request to retrieve all pages of events and returns a single list containing
# info for all events.
def get_all_events(calendar_id):
    events = []
    page_token = None
    # executes requests for a page of events while there is a valid page token
    while True:
        calendar_events = service.events().list(
                calendarId=calendar_id,
                pageToken=page_token).execute()

        for event in calendar_events['items']:
            events.append(event)

        page_token = calendar_events.get('nextPageToken')
        # breaks out of the loop if there is no token for the next page of events
        if not page_token:
            break

    return events


def get_events_for_week(calendar_id, week_start):
    week_end = (week_start + timedelta(6))
    events = []
    page_token = None
    # executes requests for a page of events while there is a valid page token
    while True:
        calendar_events = service.events().list(
            calendarId=calendar_id,
            pageToken=page_token,
            timeMin=week_start.isoformat(),
            timeMax=week_end.isoformat()).execute()

        for event in calendar_events['items']:
            events.append(event)

        page_token = calendar_events.get('nextPageToken')
        # breaks out of the loop if there is no token for the next page of events
        if not page_token:
            break

    return events


def get_events_for_current_week(calendar_id):
    today = datetime.now(timezone.utc).astimezone()
    # gets the datetime of the Sunday for the week of the current day
    week_start = today if today.isoweekday() == 7 else (today - timedelta(today.isoweekday()))
    return get_events_for_week(calendar_id, week_start)


def get_events_for_next_week(calendar_id):
    today = datetime.now(timezone.utc).astimezone()
    # gets the datetime of the Sunday for the next week of the current day
    week_start = today if today.isoweekday() == 7 else (today + timedelta(7 - today.isoweekday()))
    return get_events_for_week(calendar_id, week_start)


# Makes a request to create an event in the calendar and returns an Event resource.
def create_event(calendar_id, event_data):
    event = service.events().insert(
        calendarId=calendar_id,
        sendNotifications=True,
        body=event_data).execute()
    return event


# Deletes all of the events in the current calendar.
def clear_all_events(calendar_id):
    events = get_all_events(calendar_id)
    if len(events) == 0:
        print('No events to delete.')
    else:
        for event in events:
            try:
                res = service.events().delete(calendarId=calendar_id, eventId=event['id']).execute()
            except:
                print('An error occurred while deleting the event.')
            sleep(0.5)


def patch_event(calendar_id, event_id, event_data):
    event = service.events().patch(
        calendarId=calendar_id,
        eventId=event_id,
        body=event_data).execute()
    return event


def renew_all_events(calendar_id, end_year):
    events = get_all_events(calendar_id)
    if len(events) == 0:
        print('No events to update.')
    else:
        rrule = f'FREQ=WEEKLY;BYDAY=MO;INTERVAL=5;UNTIL={end_year}0901T040000Z'
        event_data = {
            'recurrence': [
                f'RRULE:{rrule}'
            ]
        }
        for event in events:
            print(event)
            try:
                res = patch_event(calendar_id, event['id'], event_data)
            except Exception as e:
                print(f'An error occurred while updating the event: {e}')
            sleep(0.5)
