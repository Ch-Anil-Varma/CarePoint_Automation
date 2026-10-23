import os
import time
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utilities.logger import get_logger


class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
        self.logger = get_logger(self.__class__.__name__)

    def find_element_with_fallback(self, locators, condition=EC.presence_of_element_located):
        if isinstance(locators, tuple):
            locators = [locators]
        if not locators:
            raise ValueError("At least one locator is required.")

        last_exception = None
        deadline = time.monotonic() + self.timeout
        for index, (by, value) in enumerate(locators):
            remaining_time = deadline - time.monotonic()
            if remaining_time <= 0:
                break
            locator_timeout = remaining_time / (len(locators) - index)
            try:
                return WebDriverWait(self.driver, locator_timeout).until(condition((by, value)))
            except TimeoutException as exc:
                last_exception = exc
        self.logger.error(f"All locators failed: {locators}")
        if last_exception is None:
            raise TimeoutException(f"No locator matched before the {self.timeout}-second timeout: {locators}")
        raise last_exception

    def click(self, locators):
        element = self.find_element_with_fallback(locators, EC.presence_of_element_located)
        self.scroll_into_view(element)
        self.wait.until(EC.element_to_be_clickable(element))
        element.click()

    def type_text(self, locators, text, clear_first=True):
        element = self.find_element_with_fallback(locators, EC.visibility_of_element_located)
        self.scroll_into_view(element)
        if clear_first:
            element.clear()
        element.send_keys(text)

    def select_dropdown_by_text(self, locators, visible_text):
        element = self.find_element_with_fallback(locators, EC.visibility_of_element_located)
        self.scroll_into_view(element)
        Select(element).select_by_visible_text(visible_text)

    def get_selected_dropdown_text(self, locators):
        element = self.find_element_with_fallback(locators, EC.visibility_of_element_located)
        return Select(element).first_selected_option.text.strip()

    def get_text(self, locators):
        element = self.find_element_with_fallback(locators, EC.visibility_of_element_located)
        return element.text.strip()

    def get_attribute(self, locators, attr_name):
        element = self.find_element_with_fallback(locators, EC.presence_of_element_located)
        return element.get_attribute(attr_name)

    def is_enabled(self, locators):
        element = self.find_element_with_fallback(locators, EC.presence_of_element_located)
        return element.is_enabled()

    def is_displayed(self, locators):
        try:
            element = self.find_element_with_fallback(locators, EC.visibility_of_element_located)
            return element.is_displayed()
        except TimeoutException:
            return False

    def scroll_into_view(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});", element
        )

    def set_value_via_js(self, locators, value):
        element = self.find_element_with_fallback(locators, EC.presence_of_element_located)
        self.driver.execute_script(
            "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', {bubbles: true})); arguments[0].dispatchEvent(new Event('change', {bubbles: true}));",
            element, value
        )

    def switch_to_tab(self, index):
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[index])

    def switch_to_frame(self, locators):
        frame = self.find_element_with_fallback(locators, EC.presence_of_element_located)
        self.driver.switch_to.frame(frame)

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

    def take_screenshot(self, name_prefix="screenshot"):
        screenshots_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports", "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(screenshots_dir, f"{name_prefix}_{timestamp}.png")
        self.driver.save_screenshot(filepath)
        return filepath