# -*- coding: utf-8 -*-
from app import app
from flask import request
from app import commands

@app.route('/', methods=['POST'])
def root():
    f = request.get_json()
    message = f["object"]["message"]
    text: str = message["text"]

    if text == "/nav":
        commands.make_nav(message, app.vk, app.upload)

    if text == "/sayhello":
        commands.sayhello(message, app.vk, app.upload)

    if text.startswith("/stat"):
        commands.hw1(message, app.vk, app.user_vk, app.upload)

    if text.startswith('!'):
        commands.interactive(message, app.vk, app.upload)

        

    return "ok", 200
