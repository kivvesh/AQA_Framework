from wsgiref.validate import assert_

import allure
import pytest

from src.api import User


@allure.suite('API')
@allure.feature('API')
@allure.story('User')
@allure.title('Проверка наличия-отсутствие добавленных\удаленных товаров в корзине после перезагрузки')
@pytest.mark.api
def test_get_list_users(mylogger, config):
    """Проверка получения списка пользователей"""
    user = User(config.get('API_URL'),mylogger)
    response = user.get_list_users()
    assert response.get('per_page') == len(response.get('data'))


