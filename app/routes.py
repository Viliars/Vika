from app import app


@app.route('/', methods=['POST'])
def root():
    return "ok", 200