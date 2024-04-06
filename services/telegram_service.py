import requests
import json
from utils.utils import get_processed_updates, save_processed_updates


class TelegramService:
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        self.send_url = f'https://api.telegram.org/bot{self.token}/sendMessage'
        self.updates_url = f"https://api.telegram.org/bot{self.token}/getUpdates"
        self.send_photo_url = f"https://api.telegram.org/bot{self.token}/sendPhoto"
        self.processed_ids = get_processed_updates()

    def send_message(self, message: str):
        buttons = {
            "inline_keyboard": [
                [{"text": "Was me", "callback_data": "safe"},
                 {"text": "Lock", "callback_data": "lock"},
                    {"text": "Turn off", "callback_data": "turn_off"},
                    {"text": "Capture", "callback_data": "capture"},
                    {"text": "Photo", "callback_data": "photo"}]
            ]
        }

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

    def send_photo(self, photo):
        data = {'chat_id': self.chat_id}
        files = {'photo': photo}
        try:
            return requests.post(self.send_photo_url, data=data,
                                 files=files, verify=False, timeout=10)
        except Exception:
            raise
