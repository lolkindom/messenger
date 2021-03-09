import requests


def check_name(name):
    name_json = {'name': name}
    response = requests.post('http://127.0.0.1:5000/add_user', json=name_json)
    a = response.json()
    return a['ok']
        

url = 'http://127.0.0.1:5000/send'
name = input('Введите имя: ')
while not check_name(name):
    name = input('Имя занято, введите новое имя: ')
while True:
    text = input()
    data = {
        'name': name,
        'text': text
    }
    response = requests.post(url, json=data)