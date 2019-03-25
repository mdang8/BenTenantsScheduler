import os
import json
from twilio.rest import Client


class MessagesClient:
    TWILIO_CONFIG_FILE = os.path.abspath('configs/twilio_credentials.json')
    client = None
    phone_from = ""


    def __init__(self):
        with open(self.TWILIO_CONFIG_FILE) as f:
            twilio_creds = json.load(f)
            f.close()

        self.client = Client(twilio_creds['account_sid'], twilio_creds['auth_token'])
        self.phone_from = twilio_creds['phone_number']


    def send(self, message_body, phone_to):
        message = self.client.messages \
            .create(body=message_body, from_=self.phone_from, to=phone_to)
        return message.sid
