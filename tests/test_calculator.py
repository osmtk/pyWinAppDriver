# ******************************************************************************
#
# Copyright (c) 2016 Microsoft Corporation. All rights reserved.
#
# This code is licensed under the MIT License (MIT).
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# // LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ******************************************************************************

import re

import pytest
from appium import webdriver


@pytest.mark.usefixtures("create_session")
class TestCalculator:

    @classmethod
    @pytest.fixture(scope="class")
    def create_session(cls, request):
        desired_caps = {
            "platformName": "Windows",
            # "app": "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App",
            "appTopLevelWindow": "0x1e03ea",
        }
        request.cls.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:8000',
            desired_capabilities=desired_caps
        )
        yield
        request.cls.driver.quit()

    def get_results(self):
        displaytext = self.driver.find_element_by_accessibility_id("CalculatorResults").text
        displaytext = re.search(r"\d+", displaytext).group()
        return displaytext

    def test_initialize(self):
        self.driver.find_element_by_name("Clear").click()
        self.driver.find_element_by_name("Seven").click()
        assert self.get_results() == "7"
        self.driver.find_element_by_name("Clear").click()

    def test_addition(self):
        self.driver.find_element_by_name("One").click()
        self.driver.find_element_by_name("Plus").click()
        self.driver.find_element_by_name("Seven").click()
        self.driver.find_element_by_name("Equals").click()
        assert self.get_results() == "8"

    def test_combination(self):
        self.driver.find_element_by_name("Seven").click()
        self.driver.find_element_by_name("Multiply by").click()
        self.driver.find_element_by_name("Nine").click()
        self.driver.find_element_by_name("Plus").click()
        self.driver.find_element_by_name("One").click()
        self.driver.find_element_by_name("Equals").click()
        self.driver.find_element_by_name("Divide by").click()
        self.driver.find_element_by_name("Eight").click()
        self.driver.find_element_by_name("Equals").click()
        assert self.get_results() == "8"

    def test_division(self):
        self.driver.find_element_by_name("Eight").click()
        self.driver.find_element_by_name("Eight").click()
        self.driver.find_element_by_name("Divide by").click()
        self.driver.find_element_by_name("One").click()
        self.driver.find_element_by_name("One").click()
        self.driver.find_element_by_name("Equals").click()
        assert self.get_results() == "8"

    def test_multiplication(self):
        self.driver.find_element_by_name("Nine").click()
        self.driver.find_element_by_name("Multiply by").click()
        self.driver.find_element_by_name("Nine").click()
        self.driver.find_element_by_name("Equals").click()
        assert self.get_results() == "81"

    def test_subtraction(self):
        self.driver.find_element_by_name("Nine").click()
        self.driver.find_element_by_name("Minus").click()
        self.driver.find_element_by_name("One").click()
        self.driver.find_element_by_name("Equals").click()
        assert self.get_results() == "8"
