
""" Para obtener el id del chat, se tiene que enviar un mensaje al chat del bot y acceder a 
    https://api.telegram.org/bot{{api_token}}/getUpdates
"""

from sys import exit as terminate
from services.camera_service import CameraService
from services.os_service import OSService
from services.thread_service import ThreadService
from utils.retry import retry
from services.telegram_service import TelegramService
from utils.utils import get_global_ip, get_warning_message, get_buttons
from usb.core import find as usb_find

RETRIES = None
TIME_OUT = 5

def handle_photo():
    with CameraService() as camera:
        photo = camera.take_photo()
        if not photo:
            send_msg("Camera not available")
        else:
            send_photo(photo)

def handle_action(action):
    actions = {
        "safe": lambda: terminate(0),
        "photo": lambda: handle_photo(),
        "capture": lambda: send_photo(os_service.get_screen_shot()),
        "lock": os_service.lock_screen,
        "turn_off": os_service.turn_off,
        "mute": os_service.mute_system,
        "unmute": os_service.unmute_system,
    }

    if action in actions:
        try:
            actions[action]()
        except Exception as e:
            send_msg(f"Error executing action '{action}': {e}")
    else:
        send_msg(f"Unknown action: {action}")


os_service = OSService()

vendor_id = os_service.get_environ("vendor_id")
product_id = os_service.get_environ("product_id")

vendor_id = int(vendor_id, 16) if vendor_id else None
product_id = int(product_id, 16) if product_id else None

device = usb_find(idVendor=vendor_id, idProduct=product_id)
if device:
    terminate(0)

thread_service = ThreadService()

get_global_ip_retry = retry(RETRIES, TIME_OUT)(get_global_ip)
process_response = thread_service.create_thread(get_global_ip_retry)
if not process_response:
    terminate(1)
global_ip = process_response.content.decode()

tlg_service = TelegramService(
    os_service.get_environ("tlg_api_key"),
    os_service.get_environ("chat_id")
)

send_with_retry = retry(RETRIES, TIME_OUT)(tlg_service.send_message)
send_location_with_retry = retry(RETRIES, TIME_OUT)(tlg_service.send_location)
message, lat, lon = get_warning_message(global_ip)
try:
    send_with_retry(message, buttons=get_buttons())
    send_location_with_retry(lat, lon)
except Exception:
    raise

get_updates_with_retry = retry(RETRIES, TIME_OUT)(tlg_service.process_updates)

send_msg = retry(RETRIES, TIME_OUT)(tlg_service.send_message)
send_photo = retry(RETRIES, TIME_OUT)(tlg_service.send_photo)

while True:
    try:
        action = get_updates_with_retry()
        print(f"Action: {action}")
        handle_action(action)
    except Exception as e:
        print(f"[ERROR] {e}")
