import requests
import json
from utils.utils import get_processed_updates, save_processed_updates, compress_image
from PIL import Image
from io import BytesIO

class TelegramService:
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        self.send_url = f'https://api.telegram.org/bot{self.token}/sendMessage'
        self.updates_url = f"https://api.telegram.org/bot{self.token}/getUpdates"
        self.send_photo_url = f"https://api.telegram.org/bot{self.token}/sendPhoto"
        self.send_location_url = f"https://api.telegram.org/bot{self.token}/sendLocation"
        self.processed_ids = get_processed_updates()

    def send_message(self, message: str, buttons=None):
        if not buttons:
            buttons = {}
        data = {'chat_id': self.chat_id, 'text': message,
                "reply_markup": json.dumps(buttons)}
        try:
            return requests.post(f'{self.send_url}', data=data,
                                 verify=False, timeout=10)
        except Exception:
            raise

    def process_updates(self):
        try:
            r = requests.get(self.updates_url, verify=False, timeout=10)
        except Exception:
            raise
        response = r.json()
        if not response or 'result' not in response:
            return None
        result = response['result']
        for update in result:
            if 'callback_query' not in update:
                continue
            callback_query = update['callback_query']
            callback_id = callback_query['id']
            if callback_id and callback_id not in self.processed_ids:
                self.processed_ids.append(callback_id)
                action = callback_query['data']
                save_processed_updates(self.processed_ids)
                return action
        return None

    def send_photo(self, photo_file):
        
        buffer, img_format = compress_image(photo_file)

        data = {'chat_id': self.chat_id}
        files = {'photo': ('image.' + img_format.lower(), buffer, f'image/{img_format.lower()}')}
        try:
            return requests.post(self.send_photo_url, data=data, files=files, verify=False, timeout=10)
        except Exception:
            raise

    def send_location(self, lat, lon):
        data = {'chat_id': self.chat_id, 'latitude': lat, 'longitude': lon}
        try:
            return requests.post(self.send_location_url, data=data,
                                 verify=False, timeout=10)
        except Exception:
            raise
