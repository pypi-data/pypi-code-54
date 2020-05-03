# login.py
# Ethan Guthrie
# 02/17/2020
# Creates a logged-in session to the specified TLNETCARD using the provided credentials.

from getpass import getpass
from hashlib import md5
from requests.exceptions import ConnectTimeout
from requests_html import HTMLSession
from time import sleep
from urllib3.exceptions import InsecureRequestWarning
from warnings import filterwarnings

class Login:
    # Initializes the Login object.
    def __init__(self, user="admin", passwd="password", host="", save_passwd=False, ssl=True, reject_invalid_certs=True):
        # Saving values which will be used independently.
        self._host = host
        self._user = user
        self._reject_invalid_certs = reject_invalid_certs
        self._save_passwd = save_passwd
        self._ssl = ssl
        # Checking to see if password should be saved.
        if self._save_passwd:
            self._passwd = passwd
        else:
            self._passwd = ""
        # Generating base URL.
        if ssl and self._host != "":
            self._base_url = 'https://' + self._host
        else:
            self._base_url = 'http://' + self._host
        # Executing login if a host was specified.
        if self._host != "":
            self.performLogin(passwd)
    # Returns the base URL for TLNET Supervisor.
    def getBaseURL(self):
        return self._base_url
    # Returns the host.
    def getHost(self):
        return self._host
    # Returns whether to accept invalid SSL certificates (i.e. self-signed SSL certificates).
    def getRejectInvalidCerts(self):
        return self._reject_invalid_certs
    # Returns the session.
    def getSession(self):
        return self._session
    # Closes the session.
    def logout(self):
        self._session.close()
        return
    # Logs into a new session.
    def performLogin(self, passwd):
        # Ignoring self-signed SSL certificate warning when reject_invalid_certs is False.
        if not self._reject_invalid_certs:
            filterwarnings("ignore", category=InsecureRequestWarning)       

        # Setting login URLs for future use.
        LOGIN_GET_URL = self._base_url + '/home.asp'
        LOGIN_POST_URL = self._base_url + '/delta/login'

        # Initializing session (to provide login persistence).
        session = HTMLSession()

        # Getting login screen HTML (so that Challenge can be retrieved).
        login_screen = session.get(LOGIN_GET_URL, verify=self._reject_invalid_certs, timeout=0.5)

        # Retrieving challenge from HTML.
        challenge_loc = login_screen.text.find('name="Challenge"')
        challenge = str(login_screen.text[challenge_loc + 24:challenge_loc + 32])

        # Generating 'Response' value (see login screen HTML for more details).
        response_str = self._user + passwd + challenge
        response = md5(response_str.encode('utf-8')).hexdigest()

        # Creating login payload.
        login_data = {
            'Username': self._user,
            'password': passwd,
            'Submitbtn': '      OK      ',
            'Challenge': challenge,
            'Response': response
        }

        # Logging in.
        login = session.post(LOGIN_POST_URL, data=login_data, verify=self._reject_invalid_certs)
        
        # Checking if login was successful.
        login_response = session.get(LOGIN_GET_URL, verify=self._reject_invalid_certs, timeout=0.5).text
        if login_response.find("login_title") != -1:
            print("Login failed for host at URL " + self._host)
            session.close()
            return -1

        # Restoring warnings in case reject_invalid_certs flag is used.
        filterwarnings("default", category=InsecureRequestWarning)

        # Saving session.
        self._session = session
        return
    # Sets host and then calls performLogin().
    def setHost(self, host, passwd=""):
        # Closing previous session (if there was one).
        if self._host != "":
            self.logout()
        # Saving host value.
        self._host = host
        # Setting base_url value.
        if self._ssl:
            self._base_url = 'https://' + self._host
        else:
            self._base_url = 'http://' + self._host
        # Checking if password was provided or if password was saved, and then logging in.
        if passwd != "":
            self.performLogin(passwd)
        elif self._save_passwd:
            self.performLogin(self._passwd)
        else:
            passwd = getpass()
            if self._save_passwd:
                self._passwd = passwd
            self.performLogin(getpass())
        return