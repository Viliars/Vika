from vk_api.utils import get_random_id
from rank_bm25 import BM25Okapi
import numpy as np
from app import static
import requests
import json
from numpy.random import randint


tokenized_corpus = [doc.split() for doc in static.interactive_corpus]

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
