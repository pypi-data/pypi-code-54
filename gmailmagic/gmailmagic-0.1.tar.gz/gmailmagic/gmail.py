from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().messages().list(userId='me').execute()
    id_ = [id['id'] for id in results['messages']]
    # print(id_[0])

    message = service.users().messages().get(userId='me', id=id_[0], format='raw').execute()
    msg_str = base64.urlsafe_b64decode(message['raw'])

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(msg_str, 'html.parser')
    body = soup.find_all('strong')

    # return [email.text for email in body]
    CODE = [email.text for email in body][0] #code
    CODE_SERVER = [email.text for email in body][1] #server

    return CODE, CODE_SERVER

# if __name__ == '__main__':
#     main()
