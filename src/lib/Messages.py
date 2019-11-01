import os
from json import load
from dotenv import load_dotenv
from re import search
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from src.lib.Calendar import find_calendar_id, get_events_for_current_week, get_events_for_next_week

load_dotenv()
TWILIO_CLIENT = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
PHONE_FROM = os.getenv('TWILIO_PHONE_NUMBER')
TENANTS_INFO_FILE = os.path.abspath('configs/tenants_info.json')
with open(TENANTS_INFO_FILE) as f:
    TENANTS_DATA = load(f)
    f.close()
CHORE_EMOJIS = {
    'Trash/Recycling': '🚮',
    'Dishwasher': '🍽️',
    'Kitchen Counter-tops': '🧽',
    'Kitchen Floor': '🧹',
    'Stove-tops': '🍳'
}


def send_sms(message_body, phone_to):
    message = TWILIO_CLIENT.messages.create(body=message_body, from_=PHONE_FROM, to=phone_to)
    return message.sid


def handle_reply(message_body):
    resp = MessagingResponse()
    reply_message = 'Received the message.'
    # TODO: Customize responses
    resp.message(reply_message)
    return str(resp)


def lookup_tenant_phone(name):
    return TENANTS_DATA[name]['phone']


def map_events_to_tenant():
    calendar_id = find_calendar_id('BenTenants')
    weekly_events = get_events_for_current_week(calendar_id) + get_events_for_next_week(calendar_id)
    # event summaries are formatted like: [ <name> ] - <chore>
    tenant_name_regex = '(?<=\[)(.*?)(?=\])'
    tenant_events = {}
    for event in weekly_events:
        # finds the matched string from the regex on the event summary and strips the leading and trailing whitespace
        tenant_name = search(tenant_name_regex, event['summary']).group().strip()
        event = event['summary'].split(' - ')[1]
        # append to the tenant's list of events if there already exists a key, else create one
        try:
            tenant_events[tenant_name.lower().capitalize()].append(event)
        except KeyError:
            tenant_events[tenant_name.lower().capitalize()] = [event]

    return tenant_events


def generate_event_notification_message(name, events):
    msg = f"Hello {name}! Here is your BenTenants weekly report 📋.\n\n\
Your chore for this past week was: '{events[0]}' {CHORE_EMOJIS[events[0]]} (pls do if you haven't yet!)\n\n\
Your chore for this upcoming week will be: '{events[1]}' {CHORE_EMOJIS[events[1]]}\n\n\n\
Thanks for tuning in! We'll see you next week!"
    return msg


def generate_intro_message(name):
    msg = f"Greetings {name}! I am BenTenantsScheduler, a project designed for automating the management of calendar " \
        f"events. Why am I a thing? The intention was to help make sure tenants are well notified of their upcoming " \
        f"events (chores, driveway status, etc). Also, Matt needs dumb projects like these to bolster his résumé 🤷. " \
        f"So anyways, be on the look out for my future notifications!"


def prepare_all_notification_messages(map_events):
    return map(lambda tenant: (tenant, generate_event_notification_message(tenant, map_events[tenant])), map_events)


def send_all_notifications(map_msgs):
    for x in map_msgs:
        print(x)
        tenant_phone = lookup_tenant_phone(x[0])
        if x[0] == 'Matt':
            print(f'Sending SMS message to \'{tenant_phone}\'')
            send_sms(x[1], tenant_phone)


def main():
    map_events = map_events_to_tenant()
    map_msgs = prepare_all_notification_messages(map_events)
    send_all_notifications(map_msgs)


# if __name__ == '__main__':
#     main()
