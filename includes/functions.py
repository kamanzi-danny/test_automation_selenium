"""Browser setup and the test runner for a single test case."""

import os
import time
from datetime import datetime

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from includes import constants


def create_driver():
    """Start a headless Chrome/Chromium browser."""
    options = Options()
    chrome_bin = os.environ.get("CHROME_BIN")
    if chrome_bin:
        options.binary_location = chrome_bin
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Desktop-size window so the full menu is shown (not the mobile menu).
    options.add_argument("--window-size=1366,900")

    chromedriver = "/usr/bin/chromedriver"
    if os.path.exists(chromedriver):
        service = Service(executable_path=chromedriver)
    else:
        service = Service()
    return webdriver.Chrome(service=service, options=options)


def run_test(driver, test):
    """Run one test case and return a result dictionary.

    The test never raises an error to the caller: any problem is caught
    and returned as a FAIL, so the remaining tests still run.
    """
    wait = WebDriverWait(driver, constants.WAIT_TIMEOUT)
    result = {
        "id": test["id"],
        "what": test["what"],
        "expected": describe_expected(test),
        "actual": "",
        "status": "FAIL",
        "error": "",
        "url": "",
        "screenshot": "",
        "negative": test.get("negative", False),
    }
    start = time.perf_counter()

    try:
        driver.get(constants.TEST_URL)
        try:
            # Wait for the element instead of using a fixed delay.
            element = wait.until(EC.presence_of_element_located(test["locator"]))
        except TimeoutException:
            raise AssertionError(
                f"element not found within {constants.WAIT_TIMEOUT} s "
                f"(locator: {test['locator'][1]})"
            )

        if test["check"] == "section":
            click(driver, wait, test["locator"])
            fragment = test["expected"]
            try:
                wait.until(lambda d: d.current_url.endswith(fragment))
            except TimeoutException:
                raise AssertionError(f"URL did not change to {fragment}")
            section = driver.find_element("css selector", fragment)
            if not section.is_displayed():
                raise AssertionError(f"section {fragment} is not visible")
            result["actual"] = f"URL ends {fragment}, section visible"

        elif test["check"] == "href":
            href = element.get_attribute("href")
            if href != test["expected"]:
                raise AssertionError(f"href is {href}")
            result["actual"] = f"href is {href}"

        elif test["check"] == "external":
            click(driver, wait, test["locator"])
            try:
                wait.until(lambda d: d.current_url.startswith(test["expected"]))
            except TimeoutException:
                raise AssertionError(f"browser stayed on {driver.current_url}")
            result["actual"] = f"opened {driver.current_url} (title: {driver.title})"

        result["status"] = "PASS"

    except Exception as err:  # noqa: BLE001 - record ANY failure, keep going
        # Keep only the first line: Selenium errors include a long stack trace.
        text = str(err).strip()
        message = text.splitlines()[0] if text else type(err).__name__
        message = message.removeprefix("Message: ")
        result["error"] = message
        result["actual"] = message
        result["url"] = safe_current_url(driver)
        result["screenshot"] = save_screenshot(driver, test["id"])

    result["duration"] = time.perf_counter() - start
    if not result["url"]:
        result["url"] = safe_current_url(driver)
    return result


def click(driver, wait, locator):
    """Scroll the element to the middle of the screen, wait until it is
    clickable, then click it (the fixed top menu can otherwise cover it)."""
    element = wait.until(EC.presence_of_element_located(locator))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'instant'});", element)
    wait.until(EC.element_to_be_clickable(locator)).click()


def describe_expected(test):
    """Turn a test's check into a readable expected result for the log."""
    if test["check"] == "section":
        return f"URL ends {test['expected']} and section is visible"
    if test["check"] == "href":
        return f"href is {test['expected']}"
    return f"browser opens {test['expected']}"


def safe_current_url(driver):
    try:
        return driver.current_url
    except Exception:  # noqa: BLE001
        return "unknown"


def save_screenshot(driver, test_id):
    """Save a screenshot of the page at the moment of failure."""
    try:
        os.makedirs(constants.SCREENSHOT_DIR, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(constants.SCREENSHOT_DIR, f"{test_id}_fail_{stamp}.png")
        driver.save_screenshot(path)
        return path
    except Exception:  # noqa: BLE001
        return ""
