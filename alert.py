
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

RETRIES = None
TIME_OUT = 5

os_service = OSService()

from usb.core import find as usb_find
device = usb_find(idVendor=int(os_service.get_environ("vendor_id"), 16), idProduct=int(os_service.get_environ("product_id"), 16))
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

while True:
    try:
        action = get_updates_with_retry()
        print(f"Action: {action}")
        send_photo_with_retry = retry(RETRIES, TIME_OUT)(tlg_service.send_photo)
        if action == "safe":
            terminate(0)
        elif action == "photo":
            with CameraService() as camera_service:
                photo = camera_service.take_photo()
                try:
                    if not photo:
                        send_with_retry("Camera not available")
                    else:
                        send_photo_with_retry(photo)
                except Exception:
                    raise
        elif action == "capture":
            capture = os_service.get_screen_shot()
            send_photo_with_retry(capture)
        elif action == "lock":
            os_service.lock_screen()
        elif action == "turn_off":
            os_service.turn_off()
        elif action == "mute":
            os_service.mute_system()
        elif action == "unmute":
            os_service.unmute_system()
    except Exception:
        raise
