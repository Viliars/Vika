from app import app
from flask import request

@app.route('/', methods=['POST'])
def root():
    f = request.get_json()
    #["object"]["message"]["text"]
    with open("test.txt", "wa") as fout:
        print(f, file=fout)
    return "ok", 200