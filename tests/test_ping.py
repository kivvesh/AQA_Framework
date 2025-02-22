import pytest
import allure

from src.api.base_api import BaseApi


@pytest.mark.run(order=1)
@allure.suite('API')
@allure.feature('API')
@allure.story('Service')
@allure.title('Пинг стэндов')
@pytest.mark.ui
@pytest.mark.api
def test_ping_stand(config, mylogger):
    """Пинг сервиса"""
    ui_stand = BaseApi(base_url=config.get('UI_URL'), logger=mylogger)
    response = ui_stand.ping_stand(config.get('UI_URL'))
    assert response.status_code == 200,'Стенд не доступен'
