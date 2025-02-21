import pytest
import allure

from selenium.webdriver.common.by import By

from src.pages.base_page import BasePage

class Basket(BasePage):
    """Класс страницы корзины"""
    path = 'cart.html/'

    def check_products_in_basket(self, is_availability=True):
        """Проверка наличие\отсутствие товаров в корзине"""
        test_name = self.check_products_in_basket.__doc__
        self.logger.info(test_name)
        if self.is_element((By.XPATH,'//div[@class="cart_item"]'),3) is not is_availability:
            self.logger.error(test_name)
            allure.attach(
                self.browser.get_screenshot_as_png(),
                name='Screenshot',
                attachment_type=allure.attachment_type.PNG
            )
            pytest.fail(test_name)

    def delete_all_products_from_basket(self):
        """Удаление всех товаров из корзины"""
        test_name = self.delete_all_products_from_basket.__doc__
        self.logger.info(test_name)
        for button in self.get_elements((By.XPATH,'//button[contains(text(),"Remove")]'),test_name,5):
            button.click()
