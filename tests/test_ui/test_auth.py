import pytest
import allure
import time

from src.pages import Login


@pytest.mark.run(order=1)
@allure.suite('API')
@allure.feature('API')
@allure.story('Service')
@allure.title('Пинг стэндов')
@pytest.mark.ui
def test_auth(config, mylogger, browser):
    """Проверка авторизации и выхода из системы"""
    login = Login(config.get('UI_URL'),browser,mylogger)
    login.get_corrent_path()
    login.login(config.get('UI_USER'),config.get('UI_PASSWORD'))
    login.logout()

