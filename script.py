#!/usr/local/bin/python2.7

"""
Shows basic usage of the Sheets API. Prints values from a Google Spreadsheet.
"""

from __future__ import print_function

import sys
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# Setup the Sheets API
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('sheets', 'v4', http=creds.authorize(Http()))

# put the spreadsheet id here
SPREADSHEET_ID = '1FdzAZ4Rd0RUzth1TZT0RWvAeZre6cJwwOtrw-8HY9fU'

# Make sure this range covers all of your columns. This range
# is Columns A1 through E whatever.
RANGE_NAME = 'Sheet1!A1:E'
result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                             range=RANGE_NAME).execute()
values = result.get('values', [])
if not values:
    print('No data found.')
else:
    for row in values:
        # Print columns A and E, which correspond to indices 0 and 4.
        print('%s, %s' % (row[0], row[4]))
