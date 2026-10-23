import datetime
import pytest
from pages.practice_form_page import PracticeFormPage
from utilities.data_reader import read_csv_data, read_json_data

csv_users = read_csv_data("test_users.csv")
invalid_emails = read_json_data("invalid_emails.json")

class TestWebFormAutomation:

    @pytest.mark.smoke
    def test_tc01_select_country_and_title_dropdowns(self, driver, config):
        """TC01: Verify Country and Title dropdown selection retains matching values."""
        page = PracticeFormPage(driver, config["explicit_wait"])
        page.open_form(config["base_url"])

        page.select_country("India")
        page.select_title("Dr.")

        assert page.get_selected_dropdown_text(page.COUNTRY_DROPDOWN) == "India"
        assert page.get_selected_dropdown_text(page.TITLE_DROPDOWN) == "Dr."

    @pytest.mark.smoke
    def test_tc02_select_future_joining_date(self, driver, config):
        """TC02: Calculate a dynamic future date (avoiding stale hard-coded dates) and verify input."""
        page = PracticeFormPage(driver, config["explicit_wait"])
        page.open_form(config["base_url"])

        future_date = (datetime.date.today() + datetime.timedelta(days=30)).strftime("%d/%m/%Y")
        dob_date = "1996-04-12"

        page.enter_dates(dob_date, future_date)

        assert page.get_attribute(page.DOB_INPUT, "value") == dob_date
        assert future_date in page.get_attribute(page.DOJ_INPUT, "value")

    @pytest.mark.smoke
    @pytest.mark.datadriven
    @pytest.mark.parametrize("user_data", csv_users)
    def test_tc03_submit_valid_form_data_driven(self, driver, config, user_data):
        """TC03: Fill complete valid form using synthetic CSV data and submit."""
        page = PracticeFormPage(driver, config["explicit_wait"])
        page.open_form(config["base_url"])

        user_data = {
            **user_data,
            "doj": (datetime.date.today() + datetime.timedelta(days=30)).strftime("%d/%m/%Y"),
        }
        page.fill_complete_form(user_data)

        assert page.get_selected_dropdown_text(page.COUNTRY_DROPDOWN) == user_data["country"]
        assert page.get_selected_dropdown_text(page.TITLE_DROPDOWN) == user_data["title"]
        assert page.get_attribute(page.FIRST_NAME_INPUT, "value") == user_data["first_name"]
        assert page.get_attribute(page.LAST_NAME_INPUT, "value") == user_data["last_name"]
        assert page.get_attribute(page.DOB_INPUT, "value") == user_data["dob"]
        assert page.get_attribute(page.DOJ_INPUT, "value") == user_data["doj"]
        assert page.get_attribute(page.EMAIL_INPUT, "value") == user_data["email"]
        assert page.get_selected_dropdown_text(page.PHONE_CODE_DROPDOWN) == user_data["phone_code"]

        page.click_submit()
        assert page.is_displayed(page.SUCCESS_MESSAGE)
        page.take_screenshot(f"TC03_Valid_Submit_{user_data['first_name']}")

    @pytest.mark.negative
    def test_tc04_submit_without_first_name_validation(self, driver, config):
        """TC04: Leave First Name blank and submit; verify validation prevents valid booking."""
        page = PracticeFormPage(driver, config["explicit_wait"])
        page.open_form(config["base_url"])

        user_data = {
            **csv_users[0],
            "first_name": "",
            "doj": (datetime.date.today() + datetime.timedelta(days=30)).strftime("%d/%m/%Y"),
        }
        page.fill_complete_form(user_data)
        page.click_submit()

        assert page.get_attribute(page.FIRST_NAME_INPUT, "value") == ""
        assert page.is_displayed(page.FIRST_NAME_REQUIRED_MESSAGE)

    @pytest.mark.negative
    @pytest.mark.datadriven
    @pytest.mark.parametrize("invalid_item", invalid_emails)
    def test_tc05_invalid_email_validation(self, driver, config, invalid_item):
        """TC05: Enter invalid email formats from JSON and verify validation triggers."""
        page = PracticeFormPage(driver, config["explicit_wait"])
        page.open_form(config["base_url"])

        user_data = {
            **csv_users[0],
            "email": invalid_item["email"],
            "doj": (datetime.date.today() + datetime.timedelta(days=30)).strftime("%d/%m/%Y"),
        }
        page.fill_complete_form(user_data)
        page.click_submit()

        assert (
            page.is_email_valid_html5() is False
            or page.is_displayed(page.INVALID_EMAIL_MESSAGE)
        )

    def test_tc06_communication_radio_exclusivity(self, driver, config):
        """TC06: Verify selecting Phone radio button unselects Email radio button."""
        page = PracticeFormPage(driver, config["explicit_wait"])
        page.open_form(config["base_url"])

        page.select_communication_method("Email")
        email_radio = page.find_element_with_fallback(page.RADIO_EMAIL)
        phone_radio = page.find_element_with_fallback(page.RADIO_PHONE)
        assert email_radio.is_selected() is True

        page.select_communication_method("Phone")
        assert phone_radio.is_selected() is True
        assert email_radio.is_selected() is False

    def test_tc07_clear_button_resets_form_state(self, driver, config):
        """TC07: Populate fields and click Clear button; verify fields reset reliably."""
        page = PracticeFormPage(driver, config["explicit_wait"])
        page.open_form(config["base_url"])

        page.enter_names("Arjun", "Sharma")
        page.enter_email("arjun@example.test")
        assert page.get_attribute(page.FIRST_NAME_INPUT, "value") == "Arjun"

        page.click_clear()
        assert page.get_attribute(page.FIRST_NAME_INPUT, "value") == ""
        assert page.get_attribute(page.EMAIL_INPUT, "value") == ""

    def test_tc08_check_submit_and_clear_buttons_enabled_state(self, driver, config):
        """TC08: Verify Submit and Clear buttons are visible and enabled for interaction."""
        page = PracticeFormPage(driver, config["explicit_wait"])
        page.open_form(config["base_url"])

        assert page.is_displayed(page.SUBMIT_BUTTON) is True
        assert page.is_enabled(page.SUBMIT_BUTTON) is True
        assert page.is_enabled(page.CLEAR_BUTTON) is True