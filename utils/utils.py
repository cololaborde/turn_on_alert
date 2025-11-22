from platform import system
from time import strftime
from requests import get
from json import load, dump
from io import BytesIO
from PIL.Image import open as pil_image_open, LANCZOS


def get_global_ip():
    """ get global ip retrying retries times and save data in response array """
    try:
        response = get('http://ifconfig.me', verify=False, timeout=10)
        return response
    except Exception:
        raise


def get_data_from_ip(ip):
    """ Obtener la latitud y longitud de una IP """
    try:
        response = get(
            f'http://ip-api.com/json/{ip}', verify=False, timeout=10)
        data = response.json()
        return data
    except Exception:
        raise


def get_warning_message():
    global_ip = get_global_ip().content.decode()
    ip_data = get_data_from_ip(global_ip)
    return (
        f"⚠️ Nuevo inicio detectado ⚠️\n\n"
        f"🌐 IP: {ip_data['query']} ({ip_data['city']}, {ip_data['regionName']}, {ip_data['country']})\n"
        f"📍 Ubicación: {ip_data['lat']}, {ip_data['lon']}\n"
        f"🕒 Zona horaria: {ip_data['timezone']}\n"
        f"🏢 Proveedor: {ip_data['isp']} ({ip_data['org']})\n"
        f"🖥️ Sistema: {system()}\n"
        f"📅 Fecha y hora: {strftime('%d/%m/%Y %H:%M:%S')}\n\n"
        f"🔗 Más información: https://www.infobyip.com/ip-{ip_data['query']}.html"
    ), ip_data["lat"], ip_data["lon"]

def get_buttons():
    return {
        "inline_keyboard": [[
            {"text": "🆗", "callback_data": "safe"},
            {"text": "🔒", "callback_data": "lock"},
            {"text": "OFF", "callback_data": "turn_off"},
            {"text": "🖼️", "callback_data": "capture"},
            {"text": "📷", "callback_data": "photo"},
            {"text": "🔇", "callback_data": "mute"},
            {"text": "!🔇", "callback_data": "unmute"}
            ]]
    }


def get_processed_updates():
    """ Cargar los IDs de actualizaciones procesadas desde el archivo (si existe) """
    try:
        with open('processed_ids.json', 'r') as f:
            procesados = load(f)
    except FileNotFoundError:
        procesados = []
    return procesados


def save_processed_updates(processed_ids):
    """ Guardar los IDs de actualizaciones procesadas en un archivo """
    with open('processed_ids.json', 'w') as f:
        dump(processed_ids, f, indent=4)


def compress_image(photo_file, max_size=(800, 800)):
    img = pil_image_open(photo_file)

    img.thumbnail(max_size, LANCZOS)

    buffer = BytesIO()
    img_format = img.format if img.format in ['JPEG', 'PNG'] else 'JPEG'

    img.save(buffer, format=img_format, quality=85, optimize=True)
    buffer.seek(0)
    return buffer, img_format
