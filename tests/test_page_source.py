import re

import pytest

from appium import webdriver
from src.pywinappdriver.dependencies import find_window_handle_by_regex


@pytest.mark.usefixtures("connect_driver")
class TestPageSource:

    @classmethod
    @pytest.fixture(scope="class")
    def connect_driver(cls, request):
        handle = find_window_handle_by_regex("電卓")

        caps = {
            "platformName": "Windows",
            "appTopLevelWindow": hex(handle),
            # "app": "Root",
        }
        request.cls.ms = webdriver.Remote(
            command_executor='http://127.0.0.1:4723',
            desired_capabilities=caps)
        request.cls.py = webdriver.Remote(
            command_executor='http://127.0.0.1:8000',
            desired_capabilities=caps)

    def test_compare_top_level_window_rect(self):
        ms_window = self.ms.get_window_position(self.ms.current_window_handle)
        ms_window.update(self.ms.get_window_size(self.ms.current_window_handle))
        py_window = self.py.get_window_position(self.py.current_window_handle)
        py_window.update(self.py.get_window_size(self.py.current_window_handle))
        assert py_window == ms_window
        ms_el = self.ms.find_element_by_xpath("//*")
        py_el = self.py.find_element_by_xpath("//*")
        assert py_el.rect == ms_el.rect
        ms_el = self.ms.find_element_by_xpath("//Text")
        print(ms_el.get_attribute("RuntimeId"), ms_el.get_attribute("Name"))
        py_el = self.py.find_element_by_xpath("//Text")
        print(py_el.get_attribute("RuntimeId"), py_el.get_attribute("Name"))
        assert py_el.rect == ms_el.rect

    def test_page_source(self):
        with open("ms_sample.xml", "w", encoding="utf8") as f:
            ms_page_source = self.ms.page_source
            f.write(ms_page_source)
        with open("py_sample.xml", "w", encoding="utf8") as f:
            py_page_source = self.py.page_source
            prop_to_remove = (
                "AriaProperties",
                "AriaRole",
                "BoundingRectangle",
                "ControlType",
                "Culture",
                "IsDataValidForForm",
                "NativeWindowHandle",
                "IsReadOnly",
                "CanSelectMultiple",
                "IsSelectionRequired",
                "Value",
            )
            for prop in prop_to_remove:
                py_page_source = re.sub(rf' {prop}=".*?"', "", py_page_source)
            f.write(py_page_source)
        # assert py_page_source == ms_page_source

