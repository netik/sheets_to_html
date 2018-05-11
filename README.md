1. Follow these setup instructions here...

https://developers.google.com/sheets/api/quickstart/python

2. Just like the docs say, Download the credentials file and rename it
   to 'client_secret.json'

On my mac, I have python 2.7 installed via homebrew, you might need:
   brew install python

Followed by
   pip install google-api-python-client
   pip install httplib2
   pip instlal pystache

3. Run "python script.py"

Your web browser will open to authenticate you.

This will then create a credentials.json file, which will hold your OAuth2
authentication

The HTML template is in template.mustache will be parsed and information from
the spreadsheet will be populated.

Go make a spreadsheet.
The _first row_ of the spreadsheet is the template keys.

Each row will then generate a new HTML file.
