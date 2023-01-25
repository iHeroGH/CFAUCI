import json

import imaplib
import mailbox

import datetime as dt

class Requester:

    def __init__(self):
        self.username, self.password = self.__init_creds__()
        self.__login__()

    def __init_creds__(self):
        """
        Gets the mail credentials from the credential JSON
        """
        cred_json = json.load(open('config/google_config/credentials.json'))
        return cred_json['login']['username'], cred_json['login']['password']

    def __login__(self):
        """
        Logs in to the client session
        """
        self.client = imaplib.IMAP4_SSL('imap.gmail.com')
        self.client.login(self.username, self.password)

    def get_inbox(self):
        """
        Switch the client to look through the inbox
        """
        self.client.select('inbox')

    def get_new_emails(self):
        """
        Scans for new emails from the 03260 CFA email address
        Returns a list of dicts of mail information (subject, content, html content)
        """
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

            email_data["subject"] = message["subject"].strip().replace("Fwd: ", "")

            for part in message.walk():
                content_type = part.get_content_type()

                if content_type == "text/plain":
                    body = part.get_payload(decode=True)
                    email_data['body'] = body.decode()

                elif content_type == "text/html":
                    html_body = part.get_payload(decode=True)
                    email_data['html_body'] = html_body.decode()

            all_messages.append(email_data)

        return all_messages
    
    def get_training_emails(self):
        """
        Scans for new emails from the 03260 CFA training email address
        Returns a list of dicts of mail information (subject, content, html content)
        """
        self.get_inbox()
        # The thrown var is a status check
        # Search data is a list of bytes
        _, search_data = self.client.search(None, 'FROM', '"cfa03260training@gmail.com"', "UNSEEN")

        all_messages = []
        for message_num in search_data[0].split():
            email_data = {}

            _, message_data = self.client.fetch(message_num, '(RFC822)')
            _, message_bytes = message_data[0]
            message: mailbox.MaildirMessage = mailbox.MaildirMessage(message_bytes)

            email_data["subject"] = message["subject"].strip().replace("Fwd: ", "")

            for part in message.walk():
                content_type = part.get_content_type()

                if content_type == "text/plain":
                    body = part.get_payload(decode=True)
                    email_data['body'] = body.decode()

                elif content_type == "text/html":
                    html_body = part.get_payload(decode=True)
                    email_data['html_body'] = html_body.decode()

            all_messages.append(email_data)

        return all_messages

    def get_hs_emails(self):
        """
        Scans for new emails from the HotSchedules email address
        Returns a list of dicts of mail information (subject, content, html content)
        """
        self.get_inbox()
        # The thrown var is a status check
        # Search data is a list of bytes
        _, search_data = self.client.search(None, 'FROM', '"no-reply@hotschedules.com"', "UNSEEN")

        all_messages = []
        for message_num in search_data[0].split():
            email_data = {}

            _, message_data = self.client.fetch(message_num, '(RFC822)')
            _, message_bytes = message_data[0]
            message: mailbox.MaildirMessage = mailbox.MaildirMessage(message_bytes)

            email_data["from"] = message["from"].replace(" <no-reply@hotschedules.com>", "").strip()
            email_data["subject"] = message["subject"].strip().replace("Fwd: ", "")

            for part in message.walk():
                content_type = part.get_content_type()

                if content_type == "text/plain":
                    body = part.get_payload(decode=True)
                    email_data['body'] = body.decode()

                elif content_type == "text/html":
                    html_body = part.get_payload(decode=True)
                    email_data['html_body'] = html_body.decode()

            all_messages.append(email_data)

        return all_messages

    def get_osat_emails(self, is_task: bool = True) -> dict:
        """
        Gets the most recent Quickscores email
        """

        self.get_inbox()
        # The thrown var is a status check
        # Search data is a list of bytes
        if is_task:
            _, search_data = self.client.search(None, 'FROM', "SMGMailMgr@whysmg.com", "UNSEEN")
        else:
            _, search_data = self.client.search(None, 'FROM', "SMGMailMgr@whysmg.com")

        search_data = search_data[0].split()

        if not search_data:
            return

        message_num = search_data[-1]
        _, message_data = self.client.fetch(message_num, '(RFC822)')
        _, message_bytes = message_data[0]
        message: mailbox.MaildirMessage = mailbox.MaildirMessage(message_bytes)

        email_data = {}
        if 'Date' in message.keys():
            email_data['date'] = dt.datetime.strptime(message['Date'], "%d %b %Y %H:%M:%S %z")

        for part in message.walk():
            content_type = part.get_content_type()

            if content_type == "text/plain":
                body = part.get_payload(decode=True)
                email_data['body'] = body.decode()

            elif content_type == "text/html":
                html_body = part.get_payload(decode=True)
                email_data['html_body'] = html_body.decode()

        return email_data

    def get_special_emails(self, unseen_on: bool = False) -> dict:
        """
        Get emails sent from the personal email address
        """

        self.get_inbox()
        # The thrown var is a status check
        # Search data is a list of bytes
        if unseen_on:
            _, search_data = self.client.search(None, 'FROM', "jojomedhat2004@gmail.com", "UNSEEN")
        else:
            _, search_data = self.client.search(None, 'FROM', "jojomedhat2004@gmail.com")

        all_messages = []
        for message_num in search_data[0].split():
            email_data = {}

            _, message_data = self.client.fetch(message_num, '(RFC822)')
            _, message_bytes = message_data[0]
            message: mailbox.MaildirMessage = mailbox.MaildirMessage(message_bytes)

            email_data["subject"] = message["subject"].strip().replace("Fwd: ", "")

            for part in message.walk():
                content_type = part.get_content_type()

                if content_type == "text/plain":
                    body = part.get_payload(decode=True)
                    email_data['body'] = body.decode()

                elif content_type == "text/html":
                    html_body = part.get_payload(decode=True)
                    email_data['html_body'] = html_body.decode()

            all_messages.append(email_data)

        return all_messages



