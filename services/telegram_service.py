import requests
import json
import time

class TelegramService:
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        self.send_url = f'https://api.telegram.org/bot{self.token}/sendMessage'
        self.updates_url = f"https://api.telegram.org/bot{self.token}/getUpdates"

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

        data = {'chat_id': self.chat_id, 'text': message, "reply_markup": json.dumps(buttons)}
        try:
            requests.post(f'{self.send_url}', data=data, verify=False, timeout=10)
        except Exception:
            raise


    def _process_updates(self):
        r = requests.get(self.updates_url, verify=False, timeout=10)
        response = r.json()
        if not response or 'result' not in response:
            return None
        result = response['result']
        for update in result:
            if 'callback_query' not in update:
                continue
            callback_query = update['callback_query']
            message_date = callback_query['message']['date']
            if (time.time() - message_date) < 20:
                action = callback_query['data']
                return action
        return None


    def get_updates(self):
            while True:
                action = self._process_updates()
                if action:
                    return action
                time.sleep(5)
