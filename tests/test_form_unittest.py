import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.practice_form_page import PracticeFormPage
from utilities.config_reader import load_config


class TestPracticeFormUnittest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.config = load_config()
        options = Options()
        if cls.config.get("headless", False):
            options.add_argument("--headless=new")
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.maximize_window()
        cls.page = PracticeFormPage(cls.driver, cls.config["explicit_wait"])

    def test_form_page_loads_and_populates_name(self):
        self.page.open_form(self.config["base_url"])
        self.assertIn("Practice", self.driver.title)

        self.page.enter_names("Maya", "Chen")
        actual_first = self.page.get_attribute(self.page.FIRST_NAME_INPUT, "value")
        actual_last = self.page.get_attribute(self.page.LAST_NAME_INPUT, "value")

        self.assertEqual(actual_first, "Maya", "First name input did not match")
        self.assertEqual(actual_last, "Chen", "Last name input did not match")

    @classmethod
    def tearDownClass(cls):
        if cls.driver:
            cls.driver.quit()


if __name__ == "__main__":
    unittest.main()