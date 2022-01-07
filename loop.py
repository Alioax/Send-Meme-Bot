from functions import readNames, send
from time import sleep
import json
import requests
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


bot_token = "5082514641:AAG86yy29yayXY2lky-7uo0Jk_7LCU-O9Jw"
chat_id = "-1001752203532"

CLIENT_ID = "urBJ73Tg3W8WO5cH-wKErA"
SECRET_KEY = "_jaI7Lelz3U2lvTp7empDsrCQgqz3w"


@sched.scheduled_job('interval', hours=1)
def the_code():
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

    data = {
        'grant_type': 'password',
        'username': 'alioax',
        'password': 'o91759o9576'
    }

    headers = {'User-Agent': 'MyAPI/0.0.1'}

    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=headers)
    TOKEN = res.json()['access_token']

    headers['Authorization'] = f'bearer {TOKEN}'

    res = requests.get('https://oauth.reddit.com/r/dankmemes/hot?limit=30',
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
            sleep(35)

    with open("./data/names list.json", "w") as text_file:
        json.dump(old_names + unique_names, text_file)

    print(f"{posted} messages have been sent.")


scheduler = BlockingScheduler()
scheduler.add_job(the_code, 'interval', hours=1)
scheduler.start()
