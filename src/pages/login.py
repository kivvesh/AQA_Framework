from selenium.webdriver.common.by import By

from src.pages.base_page import BasePage

class Login(BasePage):
    path=''
    def login(self,user,password):
        """Авторизация пользователя"""
        test_name = self.login.__doc__
        self.click_after_detect_element(
            (By.XPATH,'//input[@name="user-name"]'),
            test_name,
            5
        ).send_keys(user)
        self.click_after_detect_element(
            (By.XPATH, '//input[@name="password"]'),
            test_name,
            5
        ).send_keys(password)
        self.click_after_detect_element(
            (By.XPATH, '//input[@name="login-button"]'),
            test_name,
            5
        )
        assert self.is_element((By.XPATH,'//div[@id="inventory_container"]'),5)

    def logout(self):
        """Выход пользователя"""
        test_name = self.logout.__doc__
        self.click_after_detect_element(
            (By.XPATH,'//button[contains(text(),"Menu")]'),
            test_name,
            5
        )
        self.click_after_detect_element(
            (By.XPATH, '//a[contains(text(),"Logout")]'),
            test_name,
            5
        )
        assert self.is_element((By.XPATH, '//input[@name="login-button"]'),5)