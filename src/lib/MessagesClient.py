import os
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse


class MessagesClient:
    client = None
    phone_from = ""

    def __init__(self):
        self.client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
        self.phone_from = os.getenv('TWILIO_PHONE_NUMBER')

    def send(self, message_body, phone_to):
        message = self.client.messages \
            .create(body=message_body, from_=self.phone_from, to=phone_to)
        return message.sid

    def handle_reply(self, message_body):
        resp = MessagingResponse()
        reply_message = 'Received the message.'
        # TODO: Customize responses
        resp.message(reply_message)
        return str(resp)
