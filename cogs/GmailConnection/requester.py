import imaplib
import email

host = 'imap.gmail.com'

class Requester:

    def __init__(self):
        self.__login__()


    def __login__(self):
        self.mail = imaplib.IMAP4_SSL(host)
        self.mail.login('username', 'password')

    def get_inbox(self):
        self.mail.select('inbox')

