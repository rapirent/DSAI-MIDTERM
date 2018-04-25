# coding: utf-8

import requests
import json

files = {'files': open('sub-0424-3.csv', 'rb')}

with open('.token_json.json') as token_file:
    secrets = json.loads(token_file.read())

data = {
    "user_id": secrets['user_id'],   #user_id is your username which can be found on the top-right corner on our website when you logged in.
    # your team_token.
    "team_token": secrets['team_token'],
    "description": 'mean method 1 month',  #no more than 40 chars.
    "filename": "sub-0424-3.csv",  # your filename
}

url = 'https://biendata.com/competition/kdd_2018_submit/'

response = requests.post(url, files=files, data=data)

print(response.text)


