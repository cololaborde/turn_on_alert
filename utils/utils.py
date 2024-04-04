
import platform
import time
import requests


def get_global_ip():
    """ get global ip retrying retries times and save data in response array """
    try:
        response = requests.get('http://ifconfig.me', verify=False, timeout=10)
        return response
    except Exception:
        raise


def get_warning_message(global_ip: str):
    return f"Nuevo encendido desde: {global_ip} en {platform.system()} \n\n \
        Fecha y hora: {time.strftime('%d/%m/%Y %H:%M:%S')} \n\n \
        Mas información en: https://www.infobyip.com/ip-{global_ip}.html"
