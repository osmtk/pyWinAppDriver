import pytest

from appium import webdriver
from src.pywinappdriver.dependencies import find_window_handle_by_regex


class TestPageSource:

    @classmethod
    @pytest.fixture()
    def connect_driver(cls):
        handle = find_window_handle_by_regex("電卓")

        caps = {
            "platformName": "Windows",
            "appTopLevelWindow": hex(handle),
        }
        cls.ms = webdriver.Remote(
            command_executor='http://127.0.0.1:4723',
            desired_capabilities=caps)
        cls.py = webdriver.Remote(
            command_executor='http://127.0.0.1:8000',
            desired_capabilities=caps)

    def test_compare_top_level_window_rect(self, connect_driver):
        ms_el = self.ms.find_element_by_xpath("//*")
        ms_window = self.ms.get_window_position(self.ms.current_window_handle)
        ms_window.update(self.ms.get_window_size(self.ms.current_window_handle))
        py_el = self.py.find_element_by_xpath("//*")
        py_window = self.py.get_window_position(self.py.current_window_handle)
        py_window.update(self.py.get_window_size(self.py.current_window_handle))
        assert ms_window == py_window
        assert ms_el.rect == py_el.rect

