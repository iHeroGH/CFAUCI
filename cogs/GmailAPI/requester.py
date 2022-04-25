from cogs.GmailAPI.google_source import authenticate
# from google_source import authenticate

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class Requester:

    def __init__(self):
        self.creds = authenticate.auth_flow()
        self.service = self.build_service()

    def build_service(self):
        return build('gmail', 'v1', credentials=self.creds)

    def get_users(self):
        return self.service.users()

    def get_labels(self):
        results = self.get_users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        return labels

    def get_partial_message_list(self):
        results = self.get_users().messages().list(userId="me").execute()
        messages = results.get('messages', [])

        return messages

    def get_message(self, message_id):
        return self.get_users().messages().get(userId="me", id=message_id, format='raw').execute()

if __name__ == "__main__":
    print(Requester().get_message("17ec7147691597e5")['raw'])