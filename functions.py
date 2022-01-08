import requests
import constants as C


def readNames(string):
    string = list(string)
    string[len(string) - 1] = ""
    string[len(string) - 2] = ""
    string[0] = ""
    string[1] = ""
    string = "".join(string)
    string = string.split('", "')
    return string


def send(method, caption, data="", bot_token=C.bot_token):
    if method == "sendMessage":
        payload = {'chat_id': C.chat_id, 'text': caption}
    if method == "sendPhoto":
        payload = {'chat_id': C.chat_id,
                   'caption': caption + C.post_caption, 'photo': data, }
    if method == "sendVideo":
        payload = {'chat_id': C.chat_id,
                   'caption': caption + C.post_caption, 'video': data, }
    url = "https://api.telegram.org/bot" + str(bot_token) + "/" + str(method)
    r = requests.get(url, params=payload)
    if (r.status_code) == 200:
        print("a message has been sent.")
    else:
        print(f"message hasn't been sent, error: {r.text}")
