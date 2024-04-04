
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
from utils.retry import retry
from utils.thread_with_return_value import ThreadWithReturnValue
from services.telegram_service import TelegramService

RETRIES = 5
TIME_OUT = 10


@retry(RETRIES, TIME_OUT)
def get_global_ip():
    """ get global ip retrying retries times and save data in response array """
    try:
        response = requests.get('http://ifconfig.me', verify=False, timeout=10)
        return response
    except Exception:
        raise


def create_thread(function, args=None):
    thread = ThreadWithReturnValue(daemon=True, target=function, args=[] if args is None else args)
    thread.start()
    result = thread.join()
    return result


process_response = create_thread(get_global_ip)
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

send_with_retry = retry(RETRIES, TIME_OUT)(tlg_service.send_message)

try:
    send_with_retry(text)
except Exception:
    raise

get_updates_with_retry = retry(RETRIES, TIME_OUT)(tlg_service.get_updates)
try:
    action = get_updates_with_retry()
    print(f"Action: {action}")
except Exception:
    raise



# camera_service = CameraService(os.environ.get("photo_name"))
# photo = camera_service.take_photo()
