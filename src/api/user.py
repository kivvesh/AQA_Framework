import json
import allure

from pydantic import ValidationError
from requests import Response

from src.api.base_api import BaseApi
from models import ResponseDataUser, ResponsePostUser


class User(BaseApi):
    """Класс пользователя"""

    @allure.step("Получение списка пользователей")
    def get_list_users(self, *args, **kwargs) -> dict:
        """Получение списка пользователей"""
        headers = {"Content-Type": "application/json"}
        query_param = "&".join([f"{key}={value}" for key, value in kwargs])
        endpoint = f"api/users?{query_param}"
        response = self.request.get(url=f"{self.base_url}{endpoint}", headers=headers)
        assert response.status_code == 200, (
            f"Некорректны статус запроса {response.status_code}"
        )
        assert response.json().get("data"), f"Отсутствует элемент с ключом data"
        return response.json()

    @allure.step("Получение пользователя по id")
    def get_user(self, id_user: int, status=200, *args, **kwargs) -> dict | Response:
        """Получение пользователя по id"""
        headers = {"Content-Type": "application/json"}
        endpoint = f"api/users/{id_user}"
        response = self.request.get(url=f"{self.base_url}{endpoint}", headers=headers)
        if status == 200:
            assert response.status_code == 200, (
                f"Некорректны статус запроса {response.status_code}"
            )
            assert response.json().get("data"), f"Отсутствует элемент с ключом data"
            try:
                ResponseDataUser(**response.json().get("data"))
                return response.json()
            except ValidationError as error:
                assert False, (
                    f"Некорректный ответ по пользователю {response.json().get('data')} {error}"
                )
        else:
            return response

    @allure.step("Создание пользователя")
    def post_user(self, *args, **kwargs):
        """Создание пользователя"""
        headers = {"Content-Type": "application/json"}
        endpoint = f"api/users/"
        response = self.request.post(
            url=f"{self.base_url}{endpoint}", headers=headers, data=json.dumps(kwargs)
        )
        try:
            ResponsePostUser(**response.json())
            return response.json()
        except ValidationError as error:
            assert False, (
                f"Некорректный ответ по созданию пользователя {response.json()} {error}"
            )

    @allure.step("Удаление пользователя")
    def delete_user(self, user_id: int):
        """Удаление пользователя"""
        headers = {"Content-Type": "application/json"}
        endpoint = f"api/users/{user_id}"
        response = self.request.delete(
            url=f"{self.base_url}{endpoint}", headers=headers
        )
        assert response.status_code == 204, (
            f"Некорректный статус запроса {response.status_code}"
        )

    @allure.step("Регистрация пользователя")
    def post_register_user(self, status=200, *args, **kwargs):
        """Регистрация пользователя"""
        headers = {"Content-Type": "application/json"}
        endpoint = f"api/register/"
        response = self.request.post(
            url=f"{self.base_url}{endpoint}", headers=headers, data=json.dumps(kwargs)
        )
        assert response.status_code == status, (
            f"Некорректный статус запроса {response.status_code}"
        )
