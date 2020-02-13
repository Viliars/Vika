from app import app

@app.route('/', methods=['POST'])
def root():
    return "f109b7bb"