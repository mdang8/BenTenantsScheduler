# BenTenantsScheduler

Configures various apartment schedules for the BenTenants using Google Calendar and SMS notifications.

## Configuration

- `credentials.json` is required under `config/` for using the Google Calendar API.

- `calendars.json` is required under `config/`. This contains the names and ID's of the calendars to use. An example `calendars.json` is shown below:

```json
[
    {
        "id": "foo123@group.calendar.google.com",
        "name": "Foo Schedule"
    },
    {
        "id": "bar555@group.calendar.google.com",
        "name": "Bar Schedule"
    }
]
```

- `tenants_info.json` is required under `config/`. This contains the name, email, phone number, and parking order for all of the current tenants. An example `tenants_info.json` is shown below:

```json
{
  "Michael": {
    "email": "michael@foo.com",
    "phone": "5555555555",
    "parking_order": "0"
  },
  "Bob": {
    "email": "bob@foo.com",
    "phone": "0000000000",
    "parking_order": "1"
  },
  "Harold": {
    "email": "harold@foo.com",
    "phone": "3333333333",
    "parking_order": "2"
  },
  "Joe": {
    "email": "joe@foo.com",
    "phone": "5552342136",
    "parking_order": "3"
  },
  "George": {
    "email": "george@foo.com",
    "phone": "5559089642",
    "parking_order": "4"
  }
}
```

## TODO

- Add additional calendars
- Add tests / continuous integration
- Set up Twilio integration for SMS notifications
- Set up database
- Automate event operations
- Deploy to personal VPS
- Web homepage and UI management tool
