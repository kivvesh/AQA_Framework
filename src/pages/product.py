import allure

from selenium.webdriver.common.by import By

from src.pages.base_page import BasePage


class Product(BasePage):
    path = "inventory.html/"

    @allure.step("Поиск товара по названию и переход в его карточку")
    def go_to_cart_product_by_name(self, name):
        """Поиск товара по названию и переход в его карточку"""
        test_name = self.go_to_cart_product_by_name.__doc__
        self.click_after_detect_element(
            (By.XPATH, f'//a[div[contains(text(),"{name}")]]'), test_name, 5
        )

    @allure.step("Назад к каталогу товаров")
    def back_to_product(self):
        """Назад к каталогу товаров"""
        test_name = self.back_to_product.__doc__
        self.click_after_detect_element(
            (By.XPATH, f'//button[@name="back-to-products"]'), test_name, 5
        )

    @allure.step("Клик по фильтру")
    def change_filter(self, value_filter):
        """Клик по фильтру"""
        test_name = self.change_filter.__doc__
        self.click_after_detect_element(
            (By.XPATH, '//select[@class="product_sort_container"]'), test_name, 5
        )
        self.click_after_detect_element(
            (By.XPATH, f'//option[@value="{value_filter}"]'), test_name, 5
        )

    @allure.step("Получение списка имен продуктов")
    def get_list_names_products(self):
        """Получение списка имен продуктов"""
        test_name = self.get_list_names_products.__doc__
        list_products = self.get_elements(
            (By.XPATH, '//div[@class="inventory_item_name "]'), test_name, 5
        )
        return [element.text for element in list_products]

    @allure.step("Добавление товара в корзину по имени")
    def product_in_basket_by_name(self, name):
        """Добавление товара в корзину по имени"""
        test_name = self.product_in_basket_by_name.__doc__
        self.click_after_detect_element(
            (By.XPATH, f'//div[div[a[div[contains(text(), "{name}")]]]]//button'),
            test_name,
            5,
        )
