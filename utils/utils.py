import platform
import time
import requests
import json


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


def get_processed_updates():
    """ Cargar los IDs de actualizaciones procesadas desde el archivo (si existe) """
    try:
        with open('processed_ids.json', 'r') as f:
            procesados = json.load(f)
    except FileNotFoundError:
        procesados = []
    return procesados


def save_processed_updates(processed_ids):
    """ Guardar los IDs de actualizaciones procesadas en un archivo """
    with open('processed_ids.json', 'w') as f:
        json.dump(processed_ids, f, indent=4)
