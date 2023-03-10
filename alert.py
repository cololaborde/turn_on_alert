
""" Para obtener el id del chat, se tiene que enviar un mensaje al chat del bot y acceder a 
    https://api.telegram.org/bot{{api_token}}/getUpdates
"""

import os
import time
import threading
from sys import exit as terminate
import requests
from load_environ import load_environ


def send_to_telegram(message):
    """ send telegram message """
    load_environ()
    api_token = os.environ.get("tlg_api_key")
    chat_id = os.environ.get("chat_id")
    api_url = f'https://api.telegram.org/bot{api_token}/sendMessage'

    try:
        requests.post(api_url, json={'chat_id': chat_id, 'text': message}, verify=False, timeout=10)
    except Exception as exception:
        print(exception)


def get_global_ip(retries, response):
    """ get global ip retrying retries times and save data in response array """
    if retries > 0:
        try:
            response[0] = requests.get('http://ifconfig.me', verify=False, timeout=10)
            return response
        except Exception:
            time.sleep(5)
            get_global_ip(retries-1, response)
            return None
    else:
        return [None]

resp = [None]*1
t = threading.Thread(daemon=True, target=get_global_ip, args=(5, resp))
t.start()
t.join()

if not resp[0]:
    terminate()

global_ip = resp[0].content.decode()
text = f"Nuevo encendido desde: {global_ip} en Windows \n\n \
Mas información en: https://www.infobyip.com/ip-{global_ip}.html"
send_to_telegram(text)
