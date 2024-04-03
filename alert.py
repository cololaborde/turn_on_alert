
""" Para obtener el id del chat, se tiene que enviar un mensaje al chat del bot y acceder a 
    https://api.telegram.org/bot{{api_token}}/getUpdates
"""

import time
import threading
import platform
from sys import exit as terminate
import requests
from load_environ import load_environ
import os
# from services.camera_service import CameraService
from services.telegram_service import TelegramService

RETRIES = 5
TIME_OUT = 10



def get_global_ip(retries, response):
    """ get global ip retrying retries times and save data in response array """
    if retries > 0:
        try:
            response[0] = requests.get('http://ifconfig.me', verify=False, timeout=10)
            return response
        except Exception:
            time.sleep(TIME_OUT)
            get_global_ip(retries-1, response)
            return None
    else:
        return [None]


def create_thread():
    """ create a thread to try to get device's global ip in background """
    resp = [None]*1
    thread = threading.Thread(daemon=True, target=get_global_ip, args=(RETRIES, resp))
    thread.start()
    thread.join()

    if not resp[0]:
        terminate()

    return resp[0].content.decode()


global_ip = create_thread()

text = f"Nuevo encendido desde: {global_ip} en {platform.system()} \n\n \
Fecha y hora: {time.strftime('%d/%m/%Y %H:%M:%S')} \n\n \
Mas información en: https://www.infobyip.com/ip-{global_ip}.html"

load_environ()
tlg_service = TelegramService(
    os.environ.get("tlg_api_key"),
    os.environ.get("chat_id")
)

tlg_service.send_message(text)
tlg_service.get_updates()


# camera_service = CameraService(os.environ.get("photo_name"))
# photo = camera_service.take_photo()