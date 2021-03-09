import time
from datetime import datetime
import random

from flask import request, Flask

MESSAGES_LIMIT = 100

db = []
app = Flask(__name__)
victorina_settings = {
    'status': False,
    'current_answer': None,
    'victorina_QuestionID': 0
}
victorina_statisctics = {}
users = []

with open('Questions.txt', 'r') as s:
    questions = []
    for line in s:
        quest, answ = line.rstrip().split('|')
        questions.append({'Question': quest, 'Answer': answ})
    random.shuffle(questions)


def victorina_start():
    db.append({
        'id': len(db),
        'name': 'Victorina Bot',
        'text': victorina_question(),
        'timestamp': time.time()
        })
    global victorina_settings
    victorina_settings['status'] = True


def victorina_question():
    victorina_settings['victorina_QuestionID'] += 1
    victorina_settings['current_answer'] = questions[victorina_settings['victorina_QuestionID']]['Answer']
    return questions[victorina_settings['victorina_QuestionID']]['Question']


def victorina_answer(name):
    db.append({
        'id': len(db),
        'name': 'Victorina Bot',
        'text': "Правильный ответ " + victorina_settings['current_answer'] + ' участник ' +
                name + " получает 1 балл!\nСледующий вопрос:\n" + victorina_question(),
        'timestamp': time.time()
        })
    if name in victorina_statisctics:
        victorina_statisctics[name] += 1
    else:
        victorina_statisctics[name] = 1
    return {'ok': True}


@app.route("/")
def hello():
    return "Сервер мессенджера  <a href='/status'>Статус</a>" \
           " <a href='/messages'>сообщения</a>"


@app.route("/status")
def status():

    return {
        'status': True,
        'name': 'test_chat',
        'time': time.strftime('%d.%m.%Y %H:%M:%S'),
        'messages': len(db),
        'users': len(users)
    }


@app.route("/send", methods=['POST'])
def send():
    data = request.json

    db.append({
        'id': len(db),
        'name': data['name'],
        'text': data['text'],
        'timestamp': time.time()
        })
    if victorina_settings['status']:
        if data['text'] == victorina_settings['current_answer']:
            victorina_answer(data['name'])
        elif data['text'] == '/статистика':
            if data['name'] in victorina_statisctics:
                db.append({
                'id': len(db),
                'name': 'Victorina Bot',
                'text': data['name'] + ' ваш результат: ' + str(victorina_statisctics[data['name']]),
                'timestamp': time.time()
            })
            else:
                db.append({
                    'id': len(db),
                    'name': 'Victorina Bot',
                    'text': data['name'] + ' вы ни разу не угадывали ответ',
                    'timestamp': time.time()
                })
    else:
        if data['text'] == '/начать викторину':
            victorina_start()

    return {'ok': True}


@app.route("/add_user", methods=['POST'])
def add_user():
    data = request.json

    if data['name'] in users:
        return {'ok': False}
    users.append(data['name'])
    return {'ok': True}


@app.route("/messages")
def messages():
    if 'after_id' in request.args:
        after_id = int(request.args['after_id']) + 1
    else:
        after_id = 0

    return {'messages': db[after_id:after_id + MESSAGES_LIMIT]}

app.run()

