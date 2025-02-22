import json

import pytest
import allure

from logging import Logger
from copy import deepcopy

from core import Request, TelegramBot


class BaseApi:
    def __init__(self, base_url:str, logger:Logger):
        self.base_url = base_url
        self.logger = logger
        self.request = Request(logger)

    @allure.step("Проверка доступности стенда {stand}")
    def ping_stand(self, stand):
        """Проверка доступности стенда {stand}"""
        doc = self.ping_stand.__doc__.format(stand=stand)
        self.logger.info(doc)
        url = stand if '5000' not in stand else f'{stand}docs'
        response = self.request.get(url,save_text=False)
        if response.status_code != 200:
            self.logger.error(doc)
            pytest.fail(doc)
        return response

    @allure.step("Проверка размерности объекта")
    def check_len_body(self,iter_object:list, number:int):
        """Проверка размерности объекта"""
        doc = self.check_len_body.__doc__
        self.logger.info(doc)
        len_obj = len(iter_object)
        if len_obj != number:
            message = f'Длина объекта - {len_obj} не соответсвует {number}'
            self.logger.error(message)
            pytest.fail(message)

    @allure.step("Проверка сортировки объекта")
    def check_sort(self, obj:list, sort_order:str, sort_field:str):
        """Проверка сортировки объекта"""
        doc = self.check_sort.__doc__
        self.logger.info(doc)
        sort_object = deepcopy(obj)
        sort_object = sorted(sort_object, key = lambda x:(x.get(sort_field),x.get('id')))
        if sort_order.upper() == 'DESC':
            sort_object.reverse()
        if sort_object != obj:
            self.logger.error(doc)
            allure.attach(
                json.dumps(obj, indent=3, ensure_ascii=False),
                name='Объект возвращенный по API',
                attachment_type=allure.attachment_type.JSON
            )
            allure.attach(
                json.dumps(sort_object, indent=3, ensure_ascii=False),
                name='Отсортированный объект',
                attachment_type=allure.attachment_type.JSON
            )
            pytest.fail(doc)

    @allure.step("Проверка наличия или отсутствия объекта в списке")
    def check_object_in_list(self, value_obj, list_values, is_value=True):
        """Проверка наличия или отсутствия объекта в списке"""
        doc = self.check_object_in_list.__doc__
        self.logger.info(doc)
        check_is_value = value_obj in list_values
        if not(check_is_value is is_value):
            self.logger.error(doc)
            pytest.fail(doc)