from vk_api.utils import get_random_id
from rank_bm25 import BM25Okapi
import numpy as np


corpus = [
    "ну да ну да пошел я нахер",
    "назад в дурку",
    "этот маленький маневр обойдется нам в 51 год",
    "ну ты глянь на себя крыса",
    "ты чево дура",
    "просто знай ты разочаровал нас троих",
    "ах ты сукин сын я в деле",
    "бузнос диас педрилас",
    "выйди отсюда разбойник"
]

cache = {}

tokenized_corpus = [doc.split(" ") for doc in corpus]

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