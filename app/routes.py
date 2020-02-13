from app import app
from flask import request

@app.route('/', methods=['POST'])
def root():
    f = request.json()
    with open("test.txt", "w") as fout:
        print(f, file=fout)
    return "ok", 200