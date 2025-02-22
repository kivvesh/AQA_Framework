from pydantic import ValidationError

from src.api.base_api import BaseApi
from models import ResponseDataUser

class User(BaseApi):
    """Класс пользователя"""
    def get_list_users(self, *args, **kwargs) -> dict:
        """Получение списка пользователей"""
        headers = {'Content-Type': 'application/json'}
        query_param = '&'.join([f'{key}={value}' for key,value in kwargs])
        endpoint=f'api/users?{query_param}'
        response = self.request.get(url=f'{self.base_url}{endpoint}',headers=headers)
        assert response.status_code == 200, f'Некорректны статус запроса {response.status_code}'
        assert response.json().get('data'), f'Отсутствует элемент с ключом data'
        return response.json()

    def get_user(self,id_user:int,*args,**kwargs) -> dict:
        """Получение пользователя по id"""
        headers = {'Content-Type': 'application/json'}
        endpoint=f'api/users/{id_user}'
        response = self.request.get(url=f'{self.base_url}{endpoint}',headers=headers)
        assert response.status_code == 200, f'Некорректны статус запроса {response.status_code}'
        assert response.json().get('data'), f'Отсутствует элемент с ключом data'
        try:
            ResponseDataUser(**response.json().get('data'))
            return response.json()
        except ValidationError as error:
            assert False,f'Некорректный ответ по пользователю {response.json().get("data")}'
