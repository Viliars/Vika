from app import app
from flask import request

@app.route('/', methods=['POST'])
def root():
    text = request["object"]["message"]["text"]
    with open("test.txt", "wa") as fout:
        print(text, file=fout)
    return "ok", 200