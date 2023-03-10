import requests

def send_to_telegram(message):
    """ send telegram message """

    api_token = ''
    chat_id = ''
    api_url = f'https://api.telegram.org/bot{api_token}/sendMessage'

    try:
        requests.post(api_url, json={'chat_id': chat_id, 'text': message}, verify=False, timeout=10)
    except Exception as exception:
        print(exception)