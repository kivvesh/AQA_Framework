import io
import pytest
import time
import json
import allure

from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from random import randint
from logging import Logger
from datetime import datetime, timezone

from core import TelegramBot


class BasePage:
    """Базовый класс со всеми общими ui действиями в браузерами"""
    path = ''

    def __init__(self, base_url:str, browser:WebDriver, logger:Logger, tg_bot:TelegramBot):
        self.browser = browser
        self.logger = logger
        self.base_url = base_url
        self.tg_bot = tg_bot

    @allure.step('Переход по url')
    def get_corrent_path(self):
        """Переход на url"""
        time.sleep(1)
        name_action = f'{self.__class__.__doc__} {self.get_corrent_path.__doc__} {self.base_url}{self.path}'
        try:
            self.browser.get(f'{self.base_url}{self.path}')
            self.logger.debug(name_action)
        except Exception as error:
            self.logger.error(f'{name_action}\n{error}')
            allure.attach(
                self.browser.get_screenshot_as_png(),
                name='Screenshot',
                attachment_type=allure.attachment_type.PNG
            )

    def is_element(self, locator: tuple[str, str], timeout: int=1):
        """Проверка наличие элемента по локатору"""
        name_action = f'{self.is_element.__doc__} {locator}'
        self.logger.debug(f'{name_action}')

        try:
            element = WebDriverWait(self.browser, timeout).until(EC.visibility_of_element_located(locator))
            self.logger.debug(f'Элемент найден')
            return True
        except Exception as error:
            self.logger.debug(f'Элемент не найден')
            return False

    def get_element(self, locator: tuple[str, str], test_name:str, timeout: int=1):
        """Поиск 1-ого элемента по локатору"""
        name_action = f'{test_name} {self.get_element.__doc__} {locator}'

        try:
            element = WebDriverWait(self.browser, timeout).until(EC.visibility_of_element_located(locator))
            self.logger.debug(f'{name_action}')
            return element
        except Exception as error:
            self.logger.error(f'{name_action}\n{error}')
            self.tg_bot.send_error(f'Тест - {test_name}, url - {self.browser.current_url}')
            self.send_screenshot_with_message_to_tg(name_action)
            allure.attach(
                self.browser.get_screenshot_as_png(),
                name='Screenshot',
                attachment_type=allure.attachment_type.PNG
            )
            pytest.fail(name_action)


    def get_elements(self, locator: tuple[str, str], test_name:str, timeout: int=1):
        """Поиск массива элементов по локатору"""
        name_action = f'{test_name} {self.get_elements.__doc__} {locator}'

        try:
            elements = WebDriverWait(self.browser, timeout).until(EC.visibility_of_all_elements_located(locator))
            if len(elements) > 0:
                self.logger.debug(f'{name_action}')
                return elements
        except Exception as error:
            self.logger.error(f'{test_name} {self.__class__.__doc__} Элементы с локатором {locator} не найдены')
            self.logger.error(f'{name_action}\n{error}')
            self.tg_bot.send_error(f'Тест - {test_name}, url - {self.browser.current_url}')
            self.send_screenshot_with_message_to_tg(name_action)
            allure.attach(
                self.browser.get_screenshot_as_png(),
                name='Screenshot',
                attachment_type=allure.attachment_type.PNG
            )
            pytest.fail(name_action)


    def click_js(self, locator: tuple[str, str], test_name:str, timeout: int=1):
        """Клик на элемент с помощью js по локатору """
        name_action = f'{test_name} {self.get_elements.__doc__} {locator}'

        element = self.get_element(locator, test_name, timeout)
        try:
            self.browser.execute_script("arguments[0].click();", element)
            self.logger.debug(f'{name_action}')
        except Exception as error:
            self.logger.error(f'{test_name} {self.__class__.__doc__} Элементы с локатором {locator} не найдены')
            self.logger.error(f'{name_action}\n{error}')
            self.tg_bot.send_error(f'Тест - {test_name}, url - {self.browser.current_url}')
            self.send_screenshot_with_message_to_tg(name_action)
            allure.attach(
                self.browser.get_screenshot_as_png(),
                name='Screenshot',
                attachment_type=allure.attachment_type.PNG
            )
            pytest.fail(name_action)

    def click_element_with_offset(
            self, locator: tuple[str, str], test_name:str,
            timeout: int = 1, x_offset:int = randint(1, 10),
            y_offset:int = randint(1, 10)
    ):
        """Клик по элементу по локатору со сдвигом от центра"""
        name_action = f'{test_name} {self.click_element_with_offset.__doc__} {locator}'
        actions = ActionChains(self.browser)
        try:
            actions.move_to_element_with_offset(
                self.get_element(locator,test_name, timeout),
                x_offset,
                y_offset
            ).pause(randint(1, 2)).click().perform()
            self.logger.debug(f'{name_action}')
        except Exception as error:
            self.logger.error(f'{name_action}\n{error}')
            self.tg_bot.send_error(f'Тест - {test_name}, url - {self.browser.current_url}')
            self.send_screenshot_with_message_to_tg(name_action)
            allure.attach(
                self.browser.get_screenshot_as_png(),
                name='Screenshot',
                attachment_type=allure.attachment_type.PNG
            )
            pytest.fail(name_action)


    def scroll_to_y(self, y: int, test_name:str):
        """Скролл по y"""
        name_action = f'{test_name} {self.scroll_to_y.__doc__} - {y} px'
        try:
            self.browser.execute_script(f"window.scrollTo(0, {y});")
            self.logger.debug(f'{name_action}, состоялся')
        except Exception as error:
            self.logger.debug(f'{name_action}, не состоялся')

    def scroll_to_element(self, locator: tuple[str, str], test_name:str):
        """Скролл до элемента по локатору"""
        name_action = f'{test_name} {self.scroll_to_element.__doc__} {locator}'
        try:
            self.browser.execute_script("arguments[0].scrollIntoView(true);", self.get_element(locator))
            self.logger.debug(f'{name_action}')
        except Exception as error:
            self.logger.error(f'{name_action}\n{error}')
            self.tg_bot.send_error(f'Тест - {test_name}, url - {self.browser.current_url}')
            self.send_screenshot_with_message_to_tg(name_action)
            allure.attach(
                self.browser.get_screenshot_as_png(),
                name='Screenshot',
                attachment_type=allure.attachment_type.PNG
            )
            pytest.fail(name_action)

    def scroll_and_hold(self, element:WebElement, x_y:tuple, step:int=10):
        """Зажатия элемента и скролл"""
        name_action = f'{self.scroll_and_hold.__doc__} на {x_y}'
        actions = ActionChains(self.browser)
        actions.click_and_hold(element).perform()
        time.sleep(0.1)
        for i in range(step):
            try:
                actions.move_by_offset(x_y[0], x_y[1]).perform()
                time.sleep(0.05)
                self.logger.debug(name_action)
            except:
                break
        actions.release().perform()
        time.sleep(1)



    def scroll_event(self, delta_y:int, test_name:str):
        """Скролл по y через js код"""
        name_action = f'{self.scroll_event.__doc__} на {delta_y} px'
        scroll_event = f"""
        var evt = new WheelEvent('wheel', {{
            deltaY: {delta_y}, 
            bubbles: true,
            cancelable: true
        }});
        document.dispatchEvent(evt);
        """
        self.browser.execute_script(scroll_event)
        self.logger.debug(f'{name_action}')

    def click_after_detect_element(self, locator: tuple[str, str], test_name: str, timeout: int = 1, finish: int = 10):
        """Клик на элемент после обнаружения по локатору"""
        name_action = f'{test_name} {self.click_after_detect_element.__doc__} {locator}'
        point = 0
        while finish > point:
            try:
                element = WebDriverWait(self.browser, timeout).until(EC.element_to_be_clickable(locator))
                element.click()
                self.logger.debug(f'{name_action}')
                return element
            except Exception as error:
                point += timeout
                time.sleep(timeout)
                if point >= finish:
                    self.logger.error(f'{name_action}\n{error}')
                    self.tg_bot.send_error(f'Тест - {test_name}, url - {self.browser.current_url}')
                    self.send_screenshot_with_message_to_tg(name_action)
                    allure.attach(
                        self.browser.get_screenshot_as_png(),
                        name='Screenshot',
                        attachment_type=allure.attachment_type.PNG
                    )
                    pytest.fail(name_action)

    def save_screenshot(self, path:str, test_name:str):
        """Метод для сохранения скриншота"""
        name_action = f'{test_name} {self.save_screenshot.__doc__}'
        try:
            time.sleep(3)
            self.browser.save_screenshot(path)
            self.logger.debug(f'{name_action}')
        except Exception as error:
            self.logger.error(f'{name_action}\n{error}')


    def network_requests(self) -> list:
        """Получение всех requests во время тестов"""
        name_action = f'{self.network_requests.__doc__}'
        log_entries = self.browser.get_log('performance')
        list_requests = []
        for entry in log_entries:
            message = json.loads(entry['message'])['message']
            method = message.get('method')
            if method == 'Network.requestWillBeSent':
                list_requests.append(message['params']['request'])
        self.logger.debug(name_action)
        return list_requests

    def network_responses(self) -> list:
        """Получение всех responses во время тестов"""
        name_action = f'{self.network_responses.__doc__}'
        log_entries = self.browser.get_log('performance')
        list_responses = []
        for entry in log_entries:
            message = json.loads(entry['message'])['message']
            method = message.get('method')
            if method == 'Network.responseReceived':
                list_responses.append(message['params']['response'])
        self.logger.debug(name_action)
        return list_responses

    def check_status_response(self, date_start):
        """Проверка статусов ответов"""
        name_action = f'{self.check_status_response.__doc__}'
        for response in self.network_responses():
            date_from_response = response.get('headers').get('Date')
            status = response.get('status')
            if date_from_response and status:
                date_response =  datetime.strptime(response.get('headers').get('Date'), '%a, %d %b %Y %H:%M:%S %Z').replace(tzinfo=timezone.utc)
                if status and str(status)[0] in ('5') and date_response > date_start:
                    self.logger.error(
                        f'{name_action}, status - {status}, url - {response.get("url")}'
                    )
                    self.tg_bot.send_error(
                        f'{name_action}, status - {status}, url - {response.get("url")}'
                    )
                    pytest.fail(f'status - {status}, url - {response.get("url")}')

    def send_screenshot_with_message_to_tg(self, message):
        """Отправка скриншота в телеграмм канал с сообщением"""
        name_action = f'{self.send_screenshot_with_message_to_tg.__doc__} {message}'
        screenshot = self.browser.get_screenshot_as_png()
        photo = io.BytesIO(screenshot)
        self.tg_bot.send_photo_with_message(photo, message)
        self.logger.debug(name_action)


    def get_all_attributes(self, element) -> dict:
        """Получение всех атрибутов для элемента """
        name_action = f'{self.get_all_attributes.__doc__}'
        attributes = self.browser.execute_script("""
            var items = {};
            for (var i = 0; i < arguments[0].attributes.length; i++) {
                var item = arguments[0].attributes[i];
                items[item.name] = item.value;
            }
            return items;
        """, element)
        self.logger.debug(name_action)
        return attributes

    def sleep_loader(self):
        """Пропускаем загрузчик страны"""
        while not self.is_element((By.XPATH, "//div[@class='loader']"), 10):
            time.sleep(0.1)
        while self.is_element((By.XPATH, "//div[@class='loader']"), 10):
            time.sleep(5)

    def check_error_banner(self,  error_title='ошибка'):
        """Проверка появления баннера с ошибкой"""
        name_action = f'{self.check_error_banner.__doc__}'
        if self.is_element(
                (By.XPATH, '//div[span[contains(text(),"ошибка")]]'),
                10
            ):
            message = f'{name_action} - баннер появился'
            self.logger.error(message)
            self.send_screenshot_with_message_to_tg(message)
            allure.attach(
                self.browser.get_screenshot_as_png(),
                name='Screenshot',
                attachment_type=allure.attachment_type.PNG
            )
            pytest.fail(message)
        message = f'{name_action} - баннер не появился'
        self.logger.debug(message)

