import os

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


options = Options()
chrome_bin = os.environ.get("CHROME_BIN")
if chrome_bin:
    options.binary_location = chrome_bin
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

chromedriver = "/usr/bin/chromedriver"
service = Service(executable_path=chromedriver) if os.path.exists(chromedriver) else Service()
driver = webdriver.Chrome(service=service, options=options)


def test_click_item(test_url, target_url, itemname):
    try:
        driver.get(test_url)
        link_element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, itemname))
        )
        link_element.click()
        WebDriverWait(driver, 10).until(
            lambda browser: browser.current_url == target_url
        )
        print(f"Link test for {itemname} passed: {driver.current_url}")
        return "PASS"
    except TimeoutException as err:
        print(f"Timed out testing {itemname}: {err}")
        print("Current URL:", driver.current_url)
        print("Available links:", [link.text for link in driver.find_elements(By.TAG_NAME, "a")])
        return "FAIL"
    except Exception as err:
        print(f"Error testing {itemname}: {err}")
        return "FAIL"


def close_browser():
    driver.quit()
