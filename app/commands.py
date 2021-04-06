from vk_api.utils import get_random_id
from rank_bm25 import BM25Okapi
import numpy as np
from app import static
import requests
import json
from numpy.random import randint
import re
from collections import Counter, defaultdict
from datetime import datetime
import matplotlib.pyplot as plt


tokenized_corpus = [doc.split() for doc in static.interactive_corpus]
regex = re.compile("\d+")

cache = {}

bm25 = BM25Okapi(tokenized_corpus)

def sayhello(message, vk, upload):
    peer_id = message["peer_id"]
    vk.messages.send(
        message=u'Привет, я Вика - новый бот, названный в честь виртуального помощника из романа Сергея Лукьяненко "Лабиринт отражений"',
        random_id=get_random_id(),
        peer_id=peer_id
    )

def interactive(message, vk, upload):
    text: str = message["text"]
    peer_id = message["peer_id"]
    phrase: str = text[1:].strip().split()
    number = np.argmax(bm25.get_scores(phrase))

    if number in cache:
        attachment = f"photo{cache[number]['owner_id']}_{cache[number]['id']}"
    else:
        photos = upload.photo_messages(photos=f"images/{number}.jpg")
        photo = photos[0]
        attachment = f"photo{photo['owner_id']}_{photo['id']}"
        cache[number] = {'owner_id': photo['owner_id'], 'id': photo['id']}

    vk.messages.send(peer_id=peer_id, attachment=attachment, random_id=get_random_id())


def make_nav(message, vk, upload):
    peer_id = message["peer_id"]
    info = vk.messages.getConversationMembers(peer_id=peer_id)['profiles']
    rd = randint(0, len(info))
    name = f"{info[rd]['first_name']} {info[rd]['last_name']}"

    json_data = {"name": name}
    answer = requests.post("https://navalny.lol/api/generator", json=json_data)
    file = json.loads(answer.text)['file']

    receive = requests.get(f'https://navalny.lol/output/{file}')
    with open(f'nav/{file}', 'wb') as f:
        f.write(receive.content)

    photos = upload.photo_messages(photos=f'nav/{file}')
    photo = photos[0]
    attachment = f"photo{photo['owner_id']}_{photo['id']}"
    vk.messages.send(peer_id=peer_id, attachment=attachment, random_id=get_random_id())


def hw1(message, vk, user_vk, upload):
    peer_id = message["peer_id"]
    text: str = message["text"].strip().split(' ')
    id_or_nickname = text[1]
    flag_nickname = True

    if regex.match(id_or_nickname):
        flag_nickname = False
        id_or_nickname = int(id_or_nickname)

    try:
        if flag_nickname:
            info = user_vk.wall.get(domain=id_or_nickname, count=100)
        else:
            info = user_vk.wall.get(owner_id=id_or_nickname, count=100)

        posts = info["items"]
        count = len(posts)

        counter = Counter()
        for post in posts:
            counter[datetime.fromtimestamp(post["date"]).hour] += 1

        parts = defaultdict(float)

        for i in range(0, 24, 3):
            for j in range(i, i+3):
                parts[f"{i}-{i+2}"] += counter[j] / count * 100

        keys = list(parts.keys())
        values = list(parts.values())

        x = np.arange(len(keys))
        width = 0.75

        fig, ax = plt.subplots()
        rects = ax.bar(x, values, width)

        ax.set_ylabel('% постов')
        ax.set_title('Посты по временным отрезкам')
        ax.set_xticks(x)
        ax.set_xticklabels(keys)

        fig.savefig(f"hw1/{id_or_nickname}.jpg")

        photos = upload.photo_messages(photos=f"hw1/{id_or_nickname}.jpg")
        photo = photos[0]
        attachment = f"photo{photo['owner_id']}_{photo['id']}"
        vk.messages.send(peer_id=peer_id, attachment=attachment, random_id=get_random_id())
    except:
        vk.messages.send(peer_id=peer_id, message="Какая-то ошибка", random_id=get_random_id())



    