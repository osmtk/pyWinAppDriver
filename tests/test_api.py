import pytest

from appium import webdriver
from src.pywinappdriver.dependencies import find_window_handle_by_regex


class TestAPI:

    def test_compare_top_level_window_rect(self):
        handle = find_window_handle_by_regex("電卓")
        caps = {
            "platformName": "Windows",
            "appTopLevelWindow": hex(handle),
        }
        # post: /session
        ms = webdriver.Remote(
            command_executor='http://127.0.0.1:4723',
            desired_capabilities=caps)
        py = webdriver.Remote(
            command_executor='http://127.0.0.1:8000',
            desired_capabilities=caps)
        # post: /session/session_id/element
        msel = ms.find_element_by_xpath("//*")
        pyel = ms.find_element_by_xpath("//*")
        # get: /session/session_id/element/id/size
        # get: /session/session_id/element/id/location
        assert msel.rect == pyel.rect
        # get: /session/session_id/element/id/element
        assert msel.find_element_by_xpath("//*") == pyel.find_element_by_xpath("//*")
        # get: /session/session_id/element/id/enabled
        assert msel.is_enabled() == pyel.is_enabled()
        # get: /session/session_id/element/id/attribute/{name}
        assert msel.get_attribute("Name") == pyel.get_attribute("Name")
        # get: /session/session_id/element/id/displayed
        assert msel.is_displayed() == pyel.is_displayed()
        # get: /session/session_id/element/id/text
        assert msel.text == pyel.text
        # /session/session_id/window/current/maximize
        py.maximize_window()
        assert True
        # /session/session_id/window/minimize
        py.minimize_window()
        assert True

        from pywinauto import mouse
        mouse.click()

