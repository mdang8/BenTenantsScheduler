from time import sleep
from googleapiclient.discovery import build


# Client for interacting with the Google Calendar API.
class Calendar:
    creds = None
    service = None
    id = None
    calendars_info = {}

    def __init__(self, creds, calendar_id):
        self.creds = creds
        self.service = build('calendar', 'v3', credentials=creds)
        self.id = calendar_id

    # Sets the current calendar id to a new value. Changes the calendar to interact with.
    def set_calendar_id(self, id):
        self.id = id
        return self.id

    # Makes a request to retrieve all pages of events and returns a single list containing
    # info for all events.
    def get_all_events(self):
        events = []
        page_token = None
        # executes requests for a page of events while there is a valid page token
        while True:
            calendar_events = self.service.events().list(
                    calendarId=self.id,
                    pageToken=page_token).execute()

            for event in calendar_events['items']:
                events.append(event)

            page_token = calendar_events.get('nextPageToken')
            # breaks out of the loop if there is no token for the next page of events
            if not page_token:
                break

        return events

    # Makes a request to create an event in the calendar and returns an Event resource.
    def create_event(self, event_data):
        event = self.service.events().insert(
            calendarId=self.id,
            sendNotifications=True,
            body=event_data).execute()
        return event

    # Deletes all of the events in the current calendar.
    def clear_all_events(self):
        events = self.get_all_events()
        if len(events) == 0:
            print('No events to delete.')
        else:
            for event in events:
                try:
                    res = self.service.events().delete(calendarId=self.id, eventId=event['id']).execute()
                except:
                    print('An error occurred while deleting the event.')
                sleep(1)

