import imaplib
import email

import os
import json


class Requester:

    def __init__(self):
        self.username, self.password = self.__init_creds__()
        self.__login__()

    def __init_creds__(self):
        cred_json = json.load(open('config/google_config/credentials.json'))
        return cred_json['login']['username'], cred_json['login']['password']

    def __login__(self):
        self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
        self.mail.login(self.username, self.password)

    def get_inbox(self):
        self.mail.select('inbox')

    def get_messages(self):
        # The thrown var is a status check
        # Search data is a list of bytes
        _, search_data = self.mail.search(None, 'FROM', '"jojomedhat2004@gmail.com"')

        all_messages = []
        for message_num in search_data[0].split():
            email_data = {}

            _, message_data = self.mail.fetch(message_num, '(RFC822)')
            _, message_bytes = message_data[0]
            message: email._MessageT = email.message_from_bytes(message_bytes)

            for header in ['to', 'from', 'date', 'subject']:
                email_data[header] = message[header]

            for part in message.walk():
                content_type = part.get_content_type()

                if content_type == "text/plain":
                    body = part.get_payload(decode=True)
                    email_data['body'] = body.decode()

            all_messages.append(email_data)

        return all_messages

Requester()
