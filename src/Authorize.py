import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = {
    'readonly': 'https://www.googleapis.com/auth/calendar.events.readonly',
    'write': 'https://www.googleapis.com/auth/calendar.events'
}


class Authorize:
    token_file = os.path.abspath('configs/token.pickle')
    credentials_file = os.path.abspath('configs/credentials.json')
    scopes = []


    def __init__(self, scopes):
        for scope_name in scopes:
            if scope_name in SCOPES:
                self.scopes.append(SCOPES[scope_name])


    # Creates an authorization token and saves it locally as a pickle file.
    def create_token(self):
        creds = None

        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.scopes)
                creds = flow.run_local_server()
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)

        return creds
