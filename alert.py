
""" Para obtener el id del chat, se tiene que enviar un mensaje al chat del bot y acceder a 
    https://api.telegram.org/bot{{api_token}}/getUpdates
"""

from sys import exit as terminate
from services.camera_service import CameraService
from services.os_service import OSService
from services.thread_service import ThreadService
from utils.retry import retry
from services.telegram_service import TelegramService
from utils.utils import get_global_ip, get_warning_message

RETRIES = 5
TIME_OUT = 10


thread_service = ThreadService()


get_global_ip_retry = retry(RETRIES, TIME_OUT)(get_global_ip)
process_response = thread_service.create_thread(get_global_ip_retry)
if not process_response:
    terminate(1)
global_ip = process_response.content.decode()


os_service = OSService()
tlg_service = TelegramService(
    os_service.get_environ("tlg_api_key"),
    os_service.get_environ("chat_id")
)

send_with_retry = retry(RETRIES, TIME_OUT)(tlg_service.send_message)

try:
    send_with_retry(get_warning_message(global_ip))
except Exception:
    raise

get_updates_with_retry = retry(RETRIES, TIME_OUT)(tlg_service.get_updates)
try:
    action = get_updates_with_retry()
    print(f"Action: {action}")
    send_photo_with_retry = retry(RETRIES, TIME_OUT)(tlg_service.send_photo)
    if action == "photo":
        camera_service = CameraService(os_service.get_environ("photo_name"))
        photo = camera_service.take_photo()
        try:
            send_photo_with_retry(photo)
        except Exception:
            raise
    elif action == "capture":
        capture = os_service.get_screen_shot()
        send_photo_with_retry(capture)
except Exception:
    raise
