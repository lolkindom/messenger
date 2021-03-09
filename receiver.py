import time
from datetime import datetime
import requests

url = 'http://127.0.0.1:5000/messages'
after_id = -1


def pretty_print(message):
    dt = datetime.fromtimestamp(message['timestamp'])
    dt = dt.strftime('%d.%m.%Y %H:%M:%S')
    first_line = dt + ' ' + message['name']
    print(first_line)
    print(message['text'])
    print()


while True:
    response = requests.get(url, params={'after_id': self.after_id})
    messages = response.json()['messages']
    for message in messages:
        pretty_print(message)
        after_id = message['id']
    if not messages:
        time.sleep(1)

#
# response = requests.get(url, params={'after_id': after_id})
# messages = response.json()['messages']