# -*- coding: utf-8 -*-
from app import app
from flask import request
import vk_api
from vk_api.utils import get_random_id

with open("key") as key_file:
    key = key_file.read().strip()

vk_session = vk_api.VkApi(token=key)
vk = vk_session.get_api()

@app.route('/', methods=['POST'])
def root():
    f = request.get_json()
    if f["object"]["message"]["text"] == "/sayhello":
        peer_id = f["object"]["message"]["peer_id"]
        # отправляем сообщение
        vk.messages.send(
            message=u'Привет, я Вика - новый бот, названный в честь виртуального помощника из романа Сергея Лукьяненко "Лабиринт отражений"',
            random_id=get_random_id(),
            peer_id=peer_id
        )

    return "ok", 200