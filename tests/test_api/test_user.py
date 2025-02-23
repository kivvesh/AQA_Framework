import allure
import pytest

from src.api import User


@allure.suite("API")
@allure.feature("API")
@allure.story("User")
@allure.title("Проверка получения списка пользователей")
@pytest.mark.api
def test_get_list_users(mylogger, config):
    """Проверка получения списка пользователей"""
    user = User(config.get("API_URL"), mylogger)
    response = user.get_list_users()
    assert response.get("per_page") == len(response.get("data"))


@allure.suite("API")
@allure.feature("API")
@allure.story("User")
@allure.title("Проверка информации о user по id")
@pytest.mark.api
@pytest.mark.parametrize("id", [i for i in range(1, 6)])
def test_get_user(mylogger, config, id):
    """Проверка информации о user по id"""
    user = User(config.get("API_URL"), mylogger)
    user.get_user(id)


@allure.suite("API")
@allure.feature("API")
@allure.story("User")
@allure.title("Проверка информации о user по id (negative_test)")
@pytest.mark.api
@pytest.mark.parametrize("id", [i for i in range(101, 105)])
def test_negative_get_user(mylogger, config, id):
    """Проверка информации о user по id (negative_test)"""
    user = User(config.get("API_URL"), mylogger)
    response = user.get_user(id, 404)
    assert response.status_code == 404, "Некоректный статус при несуществующем user"


@allure.suite("API")
@allure.feature("API")
@allure.story("User")
@allure.title("Создание пользователя")
@pytest.mark.api
@pytest.mark.parametrize(
    "name,job",
    [
        ("Test_user", "test_job"),
        ("admin", "admin"),
        ("person", "director"),
    ],
)
def test_post_users(mylogger, config, name, job):
    """Создание пользователя"""
    user = User(config.get("API_URL"), mylogger)
    user.post_user(name=name, job=job)


@allure.suite("API")
@allure.feature("API")
@allure.story("User")
@allure.title("Удаление пользователя")
@pytest.mark.api
@pytest.mark.parametrize("id", [i for i in range(1, 5)])
def test_delete_users(mylogger, config, id):
    """Удаление пользователя"""
    user = User(config.get("API_URL"), mylogger)
    user.delete_user(id)


@allure.suite("API")
@allure.feature("API")
@allure.story("User")
@allure.title("Регистрация пользователя")
@pytest.mark.api
@pytest.mark.parametrize(
    "email,password",
    [
        ("eve.holt@reqres.in", "test_job"),
        ("janet.weaver@reqres.in", "admin"),
        ("charles.morris@reqres.in", "director"),
    ],
)
def test_register_users(mylogger, config, email, password):
    """Регистрация пользователя"""
    user = User(config.get("API_URL"), mylogger)
    user.post_register_user(email=email, password=password)


@allure.suite("API")
@allure.feature("API")
@allure.story("User")
@allure.title("Регистрация пользователя негативный тест")
@pytest.mark.api
@pytest.mark.parametrize(
    "email,password",
    [
        ("eve.holt@reqres.in", None),
        ("no_user@reqres.in", "admin"),
        ("sdfdf@asddsdd", "asds"),
    ],
)
def test_negative_register_users(mylogger, config, email, password):
    """Регистрация пользователя негативный тест"""
    user = User(config.get("API_URL"), mylogger)
    user.post_register_user(email=email, password=password, status=400)
