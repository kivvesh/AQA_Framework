import requests
import os
import glob

from dotenv import dotenv_values

from settings import ROOT_DIR

class TelegramBot:
    def __init__(self, token, channel):
        self.token = token
        self.channel = channel
        self.base_url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        self.url_photo = f"https://api.telegram.org/bot{self.token}/sendPhoto"
        self.url_document = f"https://api.telegram.org/bot{self.token}/sendDocument"

    def send_message(self, text, disable_notification=True):
        payload = {
            'chat_id': self.channel,
            'text': text,
            'parse_mode': 'HTML',
            "disable_notification": disable_notification
        }
        response = requests.post(self.base_url, data=payload)
        return response.json()

    def send_error(self, title):
        self.send_message(
            f'<b>❌ERROR</b>\n\n'
            f'{title}',
            False
        )

    def send_binary_photo(self, photo):
        files = {'photo': ('screenshot.png', photo, 'image/png')}
        data = {'chat_id': self.channel}
        response = requests.post(self.url_photo, files=files, data=data)
        return response.json()

    def send_photo_with_message(self, photo, message):
        files = {'photo': ('screenshot.png', photo, 'image/png')}
        data = {'chat_id': self.channel, 'caption': message}
        response = requests.post(self.url_photo, files=files, data=data)
        return response.json()

    def send_logs(self, disable_notification=True):
        log_files = glob.glob(os.path.join(ROOT_DIR,'logs','*.log'))
        for log in log_files:
            data = {'chat_id': self.channel, 'caption': 'Логи', "disable_notification": disable_notification}
            with open(log, 'rb') as file:
                files = {'document': file}
                response = requests.post(self.url_document, data=data, files=files)

    def send_allure(self, disable_notification=True):
        list_report = glob.glob(os.path.join(ROOT_DIR, 'allure-report', '*.html'))
        for report in list_report:
            data = {'chat_id': self.channel, 'caption': 'Отчет', "disable_notification": disable_notification}
            with open(report, 'rb') as file:
                files = {'document': file}
                response = requests.post(self.url_document, data=data, files=files)
