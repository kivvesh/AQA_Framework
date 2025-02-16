import os.path
import time
import pytest
import os
import shutil
import allure

from selenium import webdriver
from dotenv import dotenv_values
from datetime import datetime
from uuid import uuid4

from core import Logger, TelegramBot, delete_files_in_dir
from settings import ROOT_DIR


results = {
    'passed': [],
    'failed': [],
    "skipped": []
}

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Получаем информацию о тесте
    test_info = {
        'name': item.name,
        'docstring': item.function.__doc__,
        'outcome': report.outcome,
        'duration': report.duration,
        'report': report.longrepr,
    }

    # Сохраняем результаты в соответствующий список
    if report.outcome == "passed":
        results['passed'].append(test_info)
    elif report.outcome == "failed":
        results['failed'].append(test_info)
    elif report.outcome == "skipped":
        results['skipped'].append(test_info)
    item.report = report

def pytest_addoption(parser):
    parser.addoption("--level_log", action="store", default="DEBUG",
                     help="Уровень логирования")
    parser.addoption("--browser", action="store", default="chrome",
                     help="Браузер для запуска тестов")
    parser.addoption("--headless", action="store", default=False,
                     help="Включение headless режиме")

@allure.title('Получение конфигурционного файла для тестов')
@pytest.fixture(scope='session', autouse=True)
def config(request):
    config = dotenv_values(os.path.join(ROOT_DIR,'configs','.env'))
    return config


@allure.title('Получение объекта Logger')
@pytest.fixture(scope='session')
def mylogger(request):
    level = request.config.getoption('--level_log').upper()
    logger = Logger('AutoTests', level)
    return logger.get_logger()


@allure.title('Получение сессии браузера')
@pytest.fixture(scope='function')
def browser(request):
    browser_name = request.config.getoption("--browser")
    browser_options = {
        '--headless': request.config.getoption('--headless'),
        '--disable-gpu': request.config.getoption('--headless'),
        '--window-size=1920,1080': request.config.getoption('--headless'),
        '--no-sandbox': request.config.getoption('--headless'),
        '--disable-dev-shm-usage': request.config.getoption('--headless'),
    }
    user_data_dir = os.path.join(os.getcwd(), f"user_data_{str(uuid4())}")
    os.makedirs(user_data_dir, exist_ok=True)

    if browser_name == 'chrome':
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
        for key, value in browser_options.items():
            if str(value) == 'True':
                chrome_options.add_argument(key)
        chrome_options.set_capability(
            "goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"}
        )
        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_cdp_cmd('Network.enable', {})

    driver.implicitly_wait(1)
    driver.set_window_size(1920,1080)

    yield driver

    driver.quit()

    shutil.rmtree(user_data_dir, ignore_errors=True)


# @allure.title('Получение сессии браузера с авторизацией')
# @pytest.fixture(scope='session')
# def browser_with_auth_cookies(browser, config, mylogger, tg_bot):
#     from src.pages.login import Login
#     page = Login(base_url=config.get('URL_UI'), logger=mylogger, browser=browser, tg_bot=tg_bot)
#     page.login(config.get('USERNAME'), config.get('PASSWORD'))
#     time.sleep(1)
#     return browser
#
#
# @allure.title('Получение access_token')
# @pytest.fixture(scope='session')
# def access_token(mylogger, config, tg_bot):
#     """Получение access_token"""
#     login = Login(base_url=config.get('URL_API'), logger=mylogger, tg_bot=tg_bot)
#     return login.get_access_token(config.get('USERNAME'), config.get('PASSWORD'))


@allure.title("Подготовка данных перед 1 сценарием")
@pytest.fixture(scope='session')
def data_for_1_scenario(config):
    user_data = {
        "email": config.get('NEW_EMAIL_USER'),
        "password": config.get('NEW_PASSWORD_USER'),
        "full_name": config.get('NEW_FULLNAME_USER'),
    }
    data = {
        "new_user":user_data
    }
    return data