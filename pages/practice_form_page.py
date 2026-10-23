from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class PracticeFormPage(BasePage):
    # Locator Inventory with Primary (data-testid / CSS) and Fallback (Label-relative XPath)
    COUNTRY_DROPDOWN = [
        (By.CSS_SELECTOR, "[data-testid='forms-country']"),
        (By.XPATH, "//label[contains(normalize-space(),'Country of Residence')]/following::select[1]"),
        (By.XPATH, "(//select)[1]")
    ]

    TITLE_DROPDOWN = [
        (By.CSS_SELECTOR, "[data-testid='forms-title']"),
        (By.XPATH, "//label[contains(normalize-space(),'Title')]/following::select[1]"),
        (By.XPATH, "(//select)[2]")
    ]

    FIRST_NAME_INPUT = [
        (By.CSS_SELECTOR, "[data-testid='forms-first-name'], input[name*='first' i]"),
        (By.XPATH, "//label[contains(normalize-space(),'First Name')]/following::input[1]")
    ]

    FIRST_NAME_REQUIRED_MESSAGE = [
        (By.XPATH, "//*[normalize-space()='First Name is required']")
    ]

    LAST_NAME_INPUT = [
        (By.CSS_SELECTOR, "[data-testid='forms-last-name'], input[name*='last' i]"),
        (By.XPATH, "//label[contains(normalize-space(),'Last Name')]/following::input[1]")
    ]

    DOB_INPUT = [
        (By.CSS_SELECTOR, "[data-testid='forms-dob'], input[placeholder='YYYY-MM-DD'], input[type='date']"),
        (By.XPATH, "//label[contains(normalize-space(),'Date of Birth')]/following::input[1]")
    ]

    DOJ_INPUT = [
        (By.CSS_SELECTOR, "[data-testid='forms-doj'], input[placeholder='dd/mm/yyyy']"),
        (By.XPATH, "//label[contains(normalize-space(),'Date of Joining')]/following::input[1]")
    ]

    EMAIL_INPUT = [
        (By.CSS_SELECTOR, "[data-testid='forms-email'], input[type='email'], input[name*='email' i]"),
        (By.XPATH, "//label[contains(normalize-space(),'Email Address')]/following::input[1]")
    ]

    PHONE_CODE_DROPDOWN = [
        (By.CSS_SELECTOR, "[data-testid='forms-phone-code']"),
        (By.XPATH, "//label[contains(normalize-space(),'Phone Number')]/following::select[1]"),
        (By.XPATH, "(//select)[3]")
    ]

    PHONE_NUMBER_INPUT = [
        (By.CSS_SELECTOR, "[data-testid='forms-phone'], input[type='tel']"),
        (By.XPATH, "//label[contains(normalize-space(),'Phone Number')]/following::input[1]")
    ]

    RADIO_EMAIL = [
        (By.CSS_SELECTOR, "[data-testid='forms-comm-email'], input[type='radio'][value='Email' i]"),
        (By.XPATH, "//label[contains(normalize-space(),'Email')]/input[@type='radio'] | //input[@type='radio'][following-sibling::*[contains(text(),'Email')] or preceding-sibling::*[contains(text(),'Email')]]"),
        (By.XPATH, "(//input[@type='radio'])[1]")
    ]

    RADIO_PHONE = [
        (By.CSS_SELECTOR, "[data-testid='forms-comm-phone'], input[type='radio'][value='Phone' i]"),
        (By.XPATH, "//label[contains(normalize-space(),'Phone')]/input[@type='radio']"),
        (By.XPATH, "(//input[@type='radio'])[2]")
    ]

    CLEAR_BUTTON = [
        (By.CSS_SELECTOR, "[data-testid='forms-clear'], button[type='reset']"),
        (By.XPATH, "//button[normalize-space()='Clear']")
    ]

    SUBMIT_BUTTON = [
        (By.CSS_SELECTOR, "[data-testid='forms-submit'], button[type='submit']"),
        (By.XPATH, "//button[normalize-space()='Submit']")
    ]

    SUCCESS_MESSAGE = [
        (By.XPATH, "//*[normalize-space()='Details Successfully Added!']")
    ]

    INVALID_EMAIL_MESSAGE = [
        (By.XPATH, "//*[normalize-space()='Invalid Email Address']")
    ]

    def open_form(self, url):
        self.driver.get(url)

    def select_country(self, country_name):
        self.select_dropdown_by_text(self.COUNTRY_DROPDOWN, country_name)

    def select_title(self, title_name):
        self.select_dropdown_by_text(self.TITLE_DROPDOWN, title_name)

    def enter_names(self, first_name, last_name):
        self.type_text(self.FIRST_NAME_INPUT, first_name)
        self.type_text(self.LAST_NAME_INPUT, last_name)

    def enter_dates(self, dob_yyyy_mm_dd, doj_dd_mm_yyyy):
        # Set values cleanly for both standard and HTML5 date inputs
        self.type_text(self.DOB_INPUT, dob_yyyy_mm_dd)
        if self.get_attribute(self.DOB_INPUT, "value") != dob_yyyy_mm_dd:
            self.set_value_via_js(self.DOB_INPUT, dob_yyyy_mm_dd)
        self.type_text(self.DOJ_INPUT, doj_dd_mm_yyyy)

    def enter_email(self, email):
        self.type_text(self.EMAIL_INPUT, email)

    def enter_phone(self, phone_code, phone_number):
        self.select_dropdown_by_text(self.PHONE_CODE_DROPDOWN, phone_code)
        self.type_text(self.PHONE_NUMBER_INPUT, phone_number)

    def select_communication_method(self, method="Email"):
        if method.lower() == "email":
            self.click(self.RADIO_EMAIL)
        else:
            self.click(self.RADIO_PHONE)

    def click_submit(self):
        self.click(self.SUBMIT_BUTTON)

    def click_clear(self):
        self.click(self.CLEAR_BUTTON)

    def fill_complete_form(self, data):
        self.select_country(data["country"])
        self.select_title(data["title"])
        self.enter_names(data["first_name"], data["last_name"])
        self.enter_dates(data["dob"], data["doj"])
        self.enter_email(data["email"])
        self.enter_phone(data["phone_code"], data["phone_number"])
        self.select_communication_method(data["comm_method"])

    def is_email_valid_html5(self):
        el = self.find_element_with_fallback(self.EMAIL_INPUT)
        return self.driver.execute_script("return arguments[0].checkValidity();", el)