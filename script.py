#!/usr/bin/env python

"""
Take data from a google sheet and convert it into individual html pages
"""

from __future__ import print_function

import re
import os
import sys
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import pystache

# we'll put finished HTML into this directory, in the form
# OUTPUTDIR/slug/index.html

OUTPUTDIR = "/var/www/html_beto/events"

# Setup the Sheets API
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

def get_valid_filename(s):
    """
    Return the given string converted to a string that can be used for a clean
    filename. Remove leading and trailing spaces; convert other spaces to
    underscores; and remove anything that is not an alphanumeric, dash,
    underscore, or dot.
    >>> get_valid_filename("john's portrait in 2004.jpg")
    'johns_portrait_in_2004.jpg'
    """
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

store = file.Storage('credentials.json')
creds = store.get()

if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)

service = build('sheets', 'v4', http=creds.authorize(Http()))

# put the spreadsheet id here
SPREADSHEET_ID = '1FdzAZ4Rd0RUzth1TZT0RWvAeZre6cJwwOtrw-8HY9fU'

# Make sure this value covers all of your columns. This range
# is columns A1 through E...
COLS=5

# don't touch this line, unless you named your spreadsheet something different.
# note how we calculate the final column here.
RANGE_NAME = 'Sheet1!A1:' + chr(65 + COLS)

result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                             range=RANGE_NAME).execute()
values = result.get('values', [])

keys = []

if not values:
    print('No data found.')
else:
    rownum = 0
    with open('template.moustache', 'r') as myfile:
        data = myfile.read()

    parsed = pystache.parse(unicode(data))

    for row in values:
        if rownum == 0:
            # this is the header row
            # Map the first line of the sheet to field names
            col = 0
            slugfound = False

            print(row)

            while col < COLS:
                keys.append(row[col])
                if row[col] == u'slug':
                    slugfound = True
                col = col + 1

            if slugfound == False:
                print("You must have a column defined as 'slug' or this script won't work.")
                sys.exit(1)
        else:
            # this is a data row. We start with an empty hash
            params = {}

            # and we map those fields to the previously mapped field names
            newfn = ''
            col = 0
            while col < COLS:
                params[keys[col]] = row[col]
                if keys[col] == u'slug':
                    newfn = row[col]
                col = col + 1

            # and now we render a new html page with the previously created renderer
            renderer = pystache.Renderer()

            # create the file and dump the template
            try:
                os.makedirs(os.path.join(OUTPUTDIR,newfn))
            except OSError:
                pass

            newfile = os.path.join(OUTPUTDIR, get_valid_filename(newfn), "index.html")
            f = open(newfile,'w+')
            f.write(renderer.render(parsed, params))
            f.close()

        rownum = rownum + 1
