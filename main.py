import requests
import json
from time import sleep
from apscheduler.schedulers.blocking import BlockingScheduler

from functions import readNames, send

import constants as C

sched = BlockingScheduler()


auth = requests.auth.HTTPBasicAuth(C.CLIENT_ID, C.SECRET_KEY)

headers = {'User-Agent': 'MyAPI/0.0.1'}
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=C.reddit_acc_data, headers=headers)
TOKEN = res.json()['access_token']
headers['Authorization'] = f'bearer {TOKEN}'
res = requests.get(f'https://oauth.reddit.com/r/{C.subreddit}/{C.listing}?limit={C.limit}',
                   headers=headers).json()
posts = res['data']['children']

with open('./data/names list.json') as f:
    old_names = f.readlines()
    if len(old_names) == 1:
        old_names = old_names[0]
        old_names = readNames(old_names)
unique_names = []

posted = 0

for post in posts:
    if post['data']['name'] not in old_names:
        unique_names.append(post['data']['name'])
        if 'reddit_video_preview' in post['data']['preview']:
            send('sendVideo', post['data']['title'], post['data']
                 ['preview']['reddit_video_preview']["fallback_url"])
        else:
            if str(post['data']['url_overridden_by_dest']).endswith('gif'):
                send('sendVideo', post['data']['title'],
                     post['data']['url_overridden_by_dest'])
            else:
                send('sendPhoto', post['data']['title'],
                     post['data']['url_overridden_by_dest'])
        posted = posted + 1
        sleep(C.interval)

with open("./data/names list.json", "w") as text_file:
    json.dump(old_names + unique_names, text_file)

print(f"{posted} messages have been sent.")
