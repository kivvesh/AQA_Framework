import pytest
import allure

from selenium.webdriver.common.by import By

from src.pages.base_page import BasePage

class Basket(BasePage):
    """Класс страницы корзины"""
    path = 'cart.html/'

    def check_product_in_basket_by_name(self,name):
        """Проверка наличие товара по имени"""
        test_name = self.check_product_in_basket_by_name.__doc__
        self.logger.info(test_name)
        if not self.is_element((By.XPATH,f'//div[contains(text(),"{name}") and @class="inventory_item_name"]'),3):
            self.logger.error(test_name)
            allure.attach(
                self.browser.get_screenshot_as_png(),
                name='Screenshot',
                attachment_type=allure.attachment_type.PNG
            )
            pytest.fail(test_name)

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

    def click_checkout(self):
        """Клик на checkout из страницы корзины"""
        test_name = self.click_checkout.__doc__
        self.logger.info(test_name)
        self.click_after_detect_element((By.XPATH,'//button[contains(text(),"Checkout")]'),test_name,5)

    def fill_order_form(self,*args,**kwargs):
        """Заполнение формы заказа"""
        test_name = self.fill_order_form.__doc__
        self.logger.info(test_name)
        self.get_element((By.XPATH,'//input[@name="firstName"]'),test_name,3).send_keys(kwargs.get('first_name'))
        self.get_element((By.XPATH,'//input[@name="lastName"]'),test_name,3).send_keys(kwargs.get('last_name'))
        self.get_element((By.XPATH,'//input[@name="postalCode"]'),test_name,3).send_keys(kwargs.get('zip'))
        self.click_after_detect_element((By.XPATH,'//input[@value="Continue"]'),test_name,3)

    def finish_order(self):
        """Заверишть оформление заказа"""
        test_name = self.finish_order.__doc__
        self.logger.info(test_name)
        self.click_after_detect_element((By.XPATH, '//button[@name="finish"]'), test_name, 3)
        if not self.is_element((By.XPATH,'//h2[contains(text(),"Thank you for your order!")]'), 5):
            self.logger.error(test_name)
            allure.attach(
                self.browser.get_screenshot_as_png(),
                name='Screenshot',
                attachment_type=allure.attachment_type.PNG
            )
            pytest.fail(test_name)

    def back_home(self):
        """Назад к каталогу товаров"""
        test_name = self.back_home.__doc__
        self.logger.info(test_name)
        self.click_after_detect_element((By.XPATH, '//button[@id="back-to-products"]'), test_name, 3)
