from google_source import authenticate

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class Requester:

    def __init__(self):
        self.creds = authenticate.auth_flow()

    def get_labels(self):
        try:
            # Call the Gmail API
            service = build('gmail', 'v1', credentials=self.creds)
            results = service.users().labels().list(userId='me').execute()
            labels = results.get('labels', [])

            if not labels:
                print('No labels found.')
                return
            print('Labels:')
            for label in labels:
                print(label['name'])

        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f'An error occurred: {error}')

if __name__ == "__main__":
    Requester().get_labels()