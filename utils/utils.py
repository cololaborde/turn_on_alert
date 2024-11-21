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


def get_data_from_ip(ip):
    """ Obtener la latitud y longitud de una IP """
    try:
        response = requests.get(
            f'http://ip-api.com/json/{ip}', verify=False, timeout=10)
        data = response.json()
        return data
    except Exception:
        raise


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
