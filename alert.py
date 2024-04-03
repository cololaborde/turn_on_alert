
""" Para obtener el id del chat, se tiene que enviar un mensaje al chat del bot y acceder a 
    https://api.telegram.org/bot{{api_token}}/getUpdates
"""

import time
import threading
import platform
from sys import exit as terminate
import cv2
import requests
from load_environ import load_environ
import os
from services.telegram_service import TelegramService

RETRIES = 5
TIME_OUT = 10
PHOTO_NAME = 'ptoa_rdk.png'


def take_photo():
    from os import remove
    """ try to take a photo using default cam """
    cap = cv2.VideoCapture(0)

    if not cap or not cap.isOpened():
        return None

    ret, frame = cap.read()

    if not ret:
        return None
    
    cv2.imwrite(PHOTO_NAME, frame)
    photo = open(PHOTO_NAME, 'rb')
    remove(PHOTO_NAME)
    cap.release()
    return photo



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
# picture = take_photo()
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
