import base64
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from utilities.config_reader import load_config

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default=None, help="Browser to run tests: chrome or edge")
    parser.addoption("--headless", action="store_true", default=False, help="Run browser in headless mode")

@pytest.fixture(scope="session")
def config():
    return load_config()

@pytest.fixture(scope="function")
def driver(request, config):
    browser_name = request.config.getoption("--browser") or config.get("browser", "chrome")
    headless = request.config.getoption("--headless") or config.get("headless", False)

    if browser_name.lower() == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        drv = webdriver.Chrome(options=options)
    elif browser_name.lower() == "edge":
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        drv = webdriver.Edge(options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    drv.maximize_window()
    yield drv
    drv.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshots_dir = os.path.join(os.path.dirname(__file__), "reports", "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshots_dir, f"FAIL_{item.name}.png")
            driver.save_screenshot(screenshot_path)

            pytest_html = item.config.pluginmanager.getplugin("html")
            if pytest_html:
                with open(screenshot_path, "rb") as screenshot_file:
                    screenshot_data = base64.b64encode(screenshot_file.read()).decode("ascii")
                extras.append(pytest_html.extras.image(screenshot_data))
            report.extras = extras