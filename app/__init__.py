from flask import Flask
import vk_api
from vk_api import VkUpload

with open("key") as key_file:
    key = key_file.read().strip()

app = Flask(__name__)

vk_session = vk_api.VkApi(token=key)

app.upload = VkUpload(vk_session)
app.vk = vk_session.get_api()

from app import routes