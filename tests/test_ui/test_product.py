import pytest
import allure
import time

from src.pages import Product, Login


@allure.suite("UI")
@allure.feature("UI")
@allure.story("Product")
@allure.title("Поиск товара по имени")
@pytest.mark.ui
@pytest.mark.parametrize(
    "name_cart",
    [
        "Sauce Labs Backpack",
        "Sauce Labs Bolt T-ShirtTESTTEST",
        "Sauce Labs Bike Light",
    ],
)
def test_search_and_go_to_product(config, mylogger, browser, name_cart):
    """Тест на поиск карточки товара по имени и переход в него"""
    login = Login(config.get("UI_URL"), browser, mylogger)
    login.get_corrent_path()
    login.login(config.get("UI_USER"), config.get("UI_PASSWORD"))

    product = Product(config.get("UI_URL"), login.browser, mylogger)
    product.get_corrent_path()
    product.go_to_cart_product_by_name(name_cart)
    product.back_to_product()
    # product.go_to_cart_product_by_name('Sauce Labs Bike Light')
    # product.back_to_product()
    # product.go_to_cart_product_by_name('Sauce Labs Bolt T-Shirt')
    # product.back_to_product()


@allure.suite("UI")
@allure.feature("UI")
@allure.story("Product")
@allure.title("Сортировка товаров по имени")
@pytest.mark.ui
def test_sort_products_by_name(config, mylogger, browser):
    """Тест на сортировку товаров по имени"""
    login = Login(config.get("UI_URL"), browser, mylogger)
    login.get_corrent_path()
    login.login(config.get("UI_USER"), config.get("UI_PASSWORD"))

    product = Product(config.get("UI_URL"), login.browser, mylogger)
    product.get_corrent_path()
    product.change_filter("az")
    list_names_products_az = product.get_list_names_products()
    product.change_filter("za")
    list_names_products_za = product.get_list_names_products()
    assert list_names_products_az[0] == list_names_products_za[-1], (
        "Сортировка товаров по имени не работает"
    )


@allure.suite("UI")
@allure.feature("UI")
@allure.story("Product")
@allure.title("Сортировка товаров по цене")
@pytest.mark.ui
def test_sort_products_by_price(config, mylogger, browser):
    """Тест на сортировку товаров по цене"""
    login = Login(config.get("UI_URL"), browser, mylogger)
    login.get_corrent_path()
    login.login(config.get("UI_USER"), config.get("UI_PASSWORD"))

    product = Product(config.get("UI_URL"), login.browser, mylogger)
    product.get_corrent_path()
    product.change_filter("lohi")
    list_names_products_az = product.get_list_names_products()
    product.change_filter("hilo")
    list_names_products_za = product.get_list_names_products()
    assert list_names_products_az[0] == list_names_products_za[-1], (
        "Сортировка товаров по цене не работает"
    )
