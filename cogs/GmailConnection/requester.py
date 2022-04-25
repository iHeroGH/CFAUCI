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

Requester()
