import pytest
import allure
import time

from src.pages import Product, Login, Basket


@allure.suite("UI")
@allure.feature("UI")
@allure.story("Basket")
@allure.title(
    "Проверка наличия-отсутствие добавленных\удаленных товаров в корзине после перезагрузки"
)
@pytest.mark.ui
@pytest.mark.parametrize(
    "name_cart",
    [
        "Sauce Labs BackpackTESTTEST",
        "Sauce Labs Bolt T-Shirt",
        "Sauce Labs Bike Light",
    ],
)
def test_are_products_after_reload_page(browser, config, mylogger, name_cart):
    """Проверка наличия-отсутствие добавленных\удаленных товаров в корзине после перезагрузки страницы"""
    login = Login(config.get("UI_URL"), browser, mylogger)
    login.get_corrent_path()
    login.login(config.get("UI_USER"), config.get("UI_PASSWORD"))

    basket = Basket(config.get("UI_URL"), login.browser, mylogger)
    basket.get_corrent_path()
    basket.check_products_in_basket(is_availability=False)

    product = Product(config.get("UI_URL"), login.browser, mylogger)
    product.get_corrent_path()
    product.product_in_basket_by_name(name_cart)

    basket.get_corrent_path()
    basket.check_products_in_basket()
    basket.browser.refresh()
    basket.check_products_in_basket()

    basket.delete_all_products_from_basket()
    basket.browser.refresh()
    basket.check_products_in_basket(is_availability=False)


@allure.suite("UI")
@allure.feature("UI")
@allure.story("Basket")
@allure.title(
    "Проверка наличия-отсутствие добавленных\удаленных товаров в корзине после перезагрузки"
)
@pytest.mark.ui
@pytest.mark.parametrize(
    "name_cart",
    [
        "Sauce Labs Backpack",
        "Sauce Labs Bolt T-Shirt",
        "Sauce Labs Bike Light",
    ],
)
def test_order(browser, config, mylogger, name_cart):
    """Проверка заказа товаров"""
    login = Login(config.get("UI_URL"), browser, mylogger)
    login.get_corrent_path()
    login.login(config.get("UI_USER"), config.get("UI_PASSWORD"))

    product = Product(config.get("UI_URL"), login.browser, mylogger)
    product.get_corrent_path()
    product.product_in_basket_by_name(name_cart)

    basket = Basket(config.get("UI_URL"), login.browser, mylogger)
    basket.get_corrent_path()
    basket.check_product_in_basket_by_name(name_cart)
    basket.click_checkout()
    basket.fill_order_form(
        first_name=config.get("FIRST_NAME"),
        last_name=config.get("LAST_NAME"),
        zip=config.get("ZIP"),
    )
    basket.finish_order()
    basket.back_home()
