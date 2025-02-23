import os

from dotenv import dotenv_values

from settings import ROOT_DIR
from core.send_report import TelegramBot


def send_report():
    config = dotenv_values(os.path.join(ROOT_DIR, "configs", ".env"))
    bot = TelegramBot(config.get("TOKEN_TG"), config.get("CHANNEL_ID"))
    bot.send_allure()


if __name__ == "__main__":
    send_report()
