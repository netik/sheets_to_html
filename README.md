* Follow these setup instructions here...

`https://developers.google.com/sheets/api/quickstart/python`

* Just like the docs say, Download the credentials file and rename it
   to 'client_secret.json'

On my mac, I have python 2.7 installed via homebrew, but you might need to do:

`brew install python`

Followed by

``pip install google-api-python-client``

``pip install httplib2``

``pip instlal pystache``

* Go create a spreadsheet with fields. The _first row_ of the spreadsheet are the template keys.

The field "slug" is mandatory. This will become the folder name. Edit the script and set `SPREADSHEET_ID` to the ID the URL of your google docs spreadsheet.

* Edit the HTML template, `template.moustache` The HTML template will be parsed and information from the spreadsheet will be populated. Individual files will be created inside of `html/` based on the `slug` that was provided.

* Run "python script.py"

Your web browser will open to authenticate you.

This will then create a credentials.json file, which will hold your OAuth2
authentication so you can access the spreadsheet.

Each row in your spreadsheet will generate a new directory and index.html file.

A sample spreadsheet is here:

https://docs.google.com/spreadsheets/d/1FdzAZ4Rd0RUzth1TZT0RWvAeZre6cJwwOtrw-8HY9fU/edit?usp=sharing
