from flask import Flask
import vk_api
from vk_api import VkUpload
import configparser


config = configparser.ConfigParser()
config.read('vika.ini')

login = config["vk_api"].get("login")
user_token = config["vk_api"].get("user_token")
vika_token = config["vk_api"].get("vika_token")

app = Flask(__name__)

vk_session = vk_api.VkApi(token=vika_token)
vk_user_session = vk_api.VkApi(login=login, token=user_token)

app.upload = VkUpload(vk_session)
app.vk = vk_session.get_api()
app.user_vk = vk_user_session.get_api()

from app import routes