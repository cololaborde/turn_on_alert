
""" Para obtener el id del chat, se tiene que enviar un mensaje al chat del bot y acceder a 
    https://api.telegram.org/bot{{api_token}}/getUpdates
"""

import time
import platform
from sys import exit as terminate
import requests
from load_environ import load_environ
import os
# from services.camera_service import CameraService
from utils.thread_with_return_value import ThreadWithReturnValue
from services.telegram_service import TelegramService

RETRIES = 5
TIME_OUT = 10


def get_global_ip(retries):
    """ get global ip retrying retries times and save data in response array """
    if retries > 0:
        try:
            response = requests.get(
                'http://ifconfig.me', verify=False, timeout=10)
            return response
        except Exception:
            time.sleep(TIME_OUT)
            return get_global_ip(retries-1)
    else:
        return None


def create_thread(function, args):
    thread = ThreadWithReturnValue(daemon=True, target=function, args=args)
    thread.start()
    result = thread.join()
    return result


process_response = create_thread(get_global_ip, [RETRIES])
if not process_response:
    terminate(1)
global_ip = process_response.content.decode()

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
