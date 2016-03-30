import httplib2, os, base64, email, re, csv
import os

from apiclient import discovery
from apiclient import errors
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'gmail-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def getLabel():

  credentials = getCredentials()
  http = credentials.authorize(httplib2.Http())
  service = discovery.build('gmail', 'v1', http=http)

  query='label:411-web-exp'  
  
  try:
    response = service.users().messages().list(userId="me", q=query).execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().messages().list(userId=user_id, q=query, pageToken=page_token).execute()
      messages.extend(response['messages'])

    l_id = list()
    for i in range(len(messages)):
        l_id.append(messages[i]['id'])
        
    return l_id
        
  except errors.HttpError, error:
    print 'An error occurred: %s' % error


def getData():

  credentials = getCredentials()
  http = credentials.authorize(httplib2.Http())
  service = discovery.build('gmail', 'v1', http=http)

  try:
    l_out = list()
    counter = 0
    for i in getLabel():
        s_decm = base64.urlsafe_b64decode(str(service.users().messages().get(userId="me", id=i, format='full').execute()['payload']['parts'][0]['body']['data']))
        ### ITEM 1: ENG-NAT // BOOLEAN
        s_en = re.search(r'eng-nat\:\r\n(.*?)\r', s_decm)
        ### ITEM 2: ENG-ACQ-AGE // STRING
        s_ea = re.search(r'eng-acq-age\:\r\n(.*?)\r', s_decm)
        ### ITEM 3: NAT-LANG // USER INPUT STRING
        s_nl = re.search(r'nat-lang\:\r\n(.*?)\r', s_decm)
        ### ITEM 4: AUDIO-T1 // TEST 1 AUDIO // A OR B
        s_a1 = re.search(r'audio-t1\:\r\n(.*?)\r', s_decm)
        ### ITEM 5: BALL-T1 // USER CHOICE // COORDS
        s_b1 = re.search(r'ball-t1\:\r\n(.*?)\r', s_decm)
        ### ITEM 6: AUDIO-T2 // TEST 2 AUDIO // A OR B
        s_a2 = re.search(r'audio-t2\:\r\n(.*?)\r', s_decm)
        ### ITEM 7: BALL-T2 // USER CHOICE // COORDS
        s_b2 = re.search(r'ball-t2\:\r\n(.*?)\r', s_decm)
        counter += 1
        l_pre = list()
        l_pre = [counter, s_en.group(1), s_ea.group(1), s_nl.group(1), s_a1.group(1), s_b1.group(1), s_a2.group(1) ,s_b2.group(1)]
        
        l_out.append(l_pre)#decm)


    l_head = list()
    l_head = ["NUMBER", "ENG-NAT", "ENG-ACQ-AGE", "NAT-LANG", "AUDIO-T1", "BALL-T1", "AUDIO-T2", "BALL-T2"]
    l_out.insert(0, l_head)

    with open('gmail_results.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for i in l_out:
            writer.writerow(i)

    print "Done! Wrote", len(l_out), "lines of data to gmail_results.csv"
    return l_out

  except errors.HttpError, error:
    print 'An error occurred: %s' % error


if __name__ == "__main__":
    getData()
