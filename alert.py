
""" Para obtener el id del chat, se tiene que enviar un mensaje al chat del bot y acceder a 
    https://api.telegram.org/bot{{api_token}}/getUpdates
"""

import os
import time
import threading
import platform
from sys import exit as terminate
import requests
from load_environ import load_environ


RETRIES = 5
TIME_OUT = 10
PHOTO_NAME = 'ptoa_rdk.png'


def take_photo():
    """ try to take a photo using default cam """
    import cv2
    
    cap = cv2.VideoCapture(0)

    if not cap or not cap.isOpened():
        return None

    ret, frame = cap.read()

    if not ret:
        return None
    cap.release()

    cv2.imwrite(PHOTO_NAME, frame)
    photo = open(PHOTO_NAME, 'rb')
    
    return photo


def send_to_telegram(message, photo=None):
    """ send telegram message """
    load_environ()
    api_token = os.environ.get("tlg_api_key")
    chat_id = os.environ.get("chat_id")
    api_base_url = f'https://api.telegram.org/bot{api_token}'
    data = {'chat_id': chat_id, 'text': message}
    try:
        requests.post(f'{api_base_url}/sendMessage', data=data, verify=False, timeout=10)
    except Exception as exception:
        print(exception)

    if not photo:
        return
    data = {'chat_id': chat_id}
    try:
        requests.post(f'{api_base_url}/sendPhoto', data=data, files={'photo': photo}, verify=False, timeout=10)
    except Exception as exception:
        print(exception)


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


# avoid delay to videocapture on windows
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
global_ip = create_thread()
picture = take_photo()

text = f"Nuevo encendido desde: {global_ip} en {platform.system()} \n\n \
Mas información en: https://www.infobyip.com/ip-{global_ip}.html"
send_to_telegram(text, picture)

if picture:
    picture.close()
    os.remove(PHOTO_NAME)
