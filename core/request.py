import requests
import pytest

from logging import Logger
from functools import wraps


def request_exception(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            func(self, *args, **kwargs)
        except requests.exceptions.RequestException as error:
            self.logger.error(f"RequestException {error}")
            pytest.fail(f"RequestException")

    return wrapper


def log(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)

    return wrapper


class Request:
    def __init__(self, logger: Logger):
        self.logger = logger

    def post(self, url, status="2", **kwargs):
        self.logger.debug(f"POST {url} {str(kwargs)[:1000]}")
        try:
            response = requests.post(url, **kwargs)
            if str(response.status_code)[0] != status:
                self.logger.error(f"{response.status_code} {response.text[:100]}")
            else:
                self.logger.debug(f"{response.status_code}")
            return response
        except requests.exceptions.RequestException as error:
            self.logger.error(f"RequestException {error}")
            pytest.fail(f"RequestException")

    def put(self, url, status="2", **kwargs):
        self.logger.debug(f"PUT {url} {str(kwargs)[:1000]}")
        try:
            response = requests.put(url, **kwargs)
            if str(response.status_code)[0] != status:
                self.logger.error(f"{response.status_code} {response.text[:100]}")
            else:
                self.logger.debug(f"{response.status_code}")
            return response
        except requests.exceptions.RequestException as error:
            self.logger.error(f"RequestException {error}")
            pytest.fail(f"RequestException")

    def delete(self, url, status="2", **kwargs):
        self.logger.debug(f"DELETE {url} {str(kwargs)[:1000]}")
        try:
            response = requests.delete(url, **kwargs)
            if str(response.status_code)[0] != status:
                self.logger.error(f"{response.status_code} {response.text[:100]}")
            else:
                self.logger.debug(f"{response.status_code}")
            return response
        except requests.exceptions.RequestException as error:
            self.logger.error(f"RequestException {error}")
            pytest.fail(f"RequestException")

    def get(self, url, save_text=False, status="2", **kwargs):
        self.logger.debug(f"GET {url} {str(kwargs)[:1000]}")
        try:
            response = requests.get(url, **kwargs)
            if str(response.status_code)[0] != status:
                if save_text:
                    self.logger.error(f"{response.status_code} {response.text[:100]}")
                else:
                    self.logger.error(f"{response.status_code} {response.text[:100]}")
            else:
                if save_text:
                    self.logger.debug(f"{response.status_code} {response.text[:100]}")
                else:
                    self.logger.debug(f"{response.status_code}")

            return response
        except requests.exceptions.RequestException as error:
            self.logger.error(f"RequestException {error}")
            pytest.fail(f"RequestException")
