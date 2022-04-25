import json

import imaplib
import email
import mailbox


class Requester:

    def __init__(self):
        self.username, self.password = self.__init_creds__()
        self.__login__()

    def __init_creds__(self):
        cred_json = json.load(open('config/google_config/credentials.json'))
        return cred_json['login']['username'], cred_json['login']['password']

    def __login__(self):
        self.client = imaplib.IMAP4_SSL('imap.gmail.com')
        self.client.login(self.username, self.password)

    def get_inbox(self):
        self.client.select('inbox')

    def get_messages(self):
        self.get_inbox()
        # The thrown var is a status check
        # Search data is a list of bytes
        _, search_data = self.client.search(None, 'FROM', '"03260@chick-fil-a.com"', "UNSEEN")

        all_messages = []
        for message_num in search_data[0].split():
            email_data = {}

            _, message_data = self.client.fetch(message_num, '(RFC822)')
            _, message_bytes = message_data[0]
            message: mailbox.MaildirMessage = mailbox.MaildirMessage(message_bytes)

            email_data["subject"] = message["subject"].strip("Fwd: ")

            for part in message.walk():
                content_type = part.get_content_type()

                if content_type == "text/plain":
                    body = part.get_payload(decode=True)
                    email_data['body'] = body.decode()

            all_messages.append(email_data)

        return all_messages

Requester()
