# coding: utf-8

import requests
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--day', default='1')
parser.add_argument('--month', default='1')
args = parser.parse_args()

files = {'files': open(args.month + "-" + args.day +'.csv', 'rb')}

with open('.token_json.json') as token_file:
    secrets = json.loads(token_file.read())

data = {
    "user_id": secrets['user_id'],   #user_id is your username which can be found on the top-right corner on our website when you logged in.
    # your team_token.
    "team_token": secrets['team_token'],
    "description": 'mean method',  #no more than 40 chars.
    "filename": args.month + "-" + args.day +"onemonth.csv",  # your filename
}

url = 'https://biendata.com/competition/kdd_2018_submit/'

response = requests.post(url, files=files, data=data)

print(response.text)
print('submit', args.month + "-" + args.day + "onemonth.csv")

