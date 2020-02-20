# -*- coding: utf-8 -*-
from app import app
from flask import request
import vk_api
from vk_api import VkUpload
from vk_api.utils import get_random_id
from rank_bm25 import BM25Okapi
import numpy as np

with open("key") as key_file:
    key = key_file.read().strip()

corpus = [
    "ну да ну да пошел я нахер",
    "назад в дурку",
    "этот маленький маневр обойдется нам в 51 год"
]

tokenized_corpus = [doc.split(" ") for doc in corpus]

bm25 = BM25Okapi(tokenized_corpus)

vk_session = vk_api.VkApi(token=key)
upload = VkUpload(vk_session)
vk = vk_session.get_api()

@app.route('/', methods=['POST'])
def root():
    f = request.get_json()
    text: str = f["object"]["message"]["text"]
    peer_id = f["object"]["message"]["peer_id"]
    if text == "/sayhello":
        vk.messages.send(
            message=u'Привет, я Вика - новый бот, названный в честь виртуального помощника из романа Сергея Лукьяненко "Лабиринт отражений"',
            random_id=get_random_id(),
            peer_id=peer_id
        )

    if text.startswith('!'):
        phrase: str = text[1:].strip().split()
        number = np.argmax(bm25.get_scores(phrase))

        photos = upload.photo_messages(photos=f"images/{number}.jpg")
        photo = photos[0]
        attachment = f"photo{photo['owner_id']}_{photo['id']}"

        vk.messages.send(peer_id=peer_id, attachment=attachment, random_id=get_random_id())


    return "ok", 200