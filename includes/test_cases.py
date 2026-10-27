"""Test cases for the portfolio. Each one matches a row in TEST_PLAN.md.

Fields:
  id        Unique test ID used in the test plan and the log file.
  what      What is being tested (written into the log).
  locator   How Selenium finds the element: (By.<type>, "<value>").
  check     The kind of check to run:
              "section"  - click the link, then the URL must end with
                           `expected` AND that section must be visible.
              "href"     - read the link's href; it must equal `expected`.
              "external" - click the link, then the browser must land on a
                           URL that starts with `expected`.
  expected  The expected result (see `check`).
  negative  True for a test that is EXPECTED to fail. It proves that
            failures are caught and logged as ERROR.
"""

from selenium.webdriver.common.by import By

TEST_CASES = [
    {
        "id": "TC-01",
        "what": 'Click "About" in the main menu',
        "locator": (By.CSS_SELECTOR, "#nav a.nav-link[href='#about']"),
        "check": "section",
        "expected": "#about",
    },
    {
        "id": "TC-02",
        "what": 'Click "Projects" in the main menu',
        "locator": (By.CSS_SELECTOR, "#nav a.nav-link[href='#projects']"),
        "check": "section",
        "expected": "#projects",
    },
    {
        "id": "TC-03",
        "what": 'Click "Education" in the main menu',
        "locator": (By.CSS_SELECTOR, "#nav a.nav-link[href='#education']"),
        "check": "section",
        "expected": "#education",
    },
    {
        "id": "TC-04",
        "what": 'Click "Certifications" in the main menu',
        "locator": (By.CSS_SELECTOR, "#nav a.nav-link[href='#certifications']"),
        "check": "section",
        "expected": "#certifications",
    },
    {
        "id": "TC-05",
        "what": 'Click "Contact" in the main menu',
        "locator": (By.CSS_SELECTOR, "#nav a.nav-link[href='#contact']"),
        "check": "section",
        "expected": "#contact",
    },
    {
        "id": "TC-06",
        "what": 'Click the "View projects" button at the top of the page',
        "locator": (By.LINK_TEXT, "View projects"),
        "check": "section",
        "expected": "#projects",
    },
    {
        "id": "TC-07",
        "what": "Email link in the Contact section",
        "locator": (By.CSS_SELECTOR, "#contact a[href^='mailto:']"),
        "check": "href",
        "expected": "mailto:kamanzidanny5@gmail.com",
    },
    {
        "id": "TC-08",
        "what": "LinkedIn icon link in the Contact section",
        "locator": (By.CSS_SELECTOR, "#contact a[aria-label='LinkedIn']"),
        "check": "href",
        "expected": "https://www.linkedin.com/in/kamanzi-s-252880196/",
    },
    {
        "id": "TC-09",
        "what": "Click the GitHub icon link in the Contact section",
        "locator": (By.CSS_SELECTOR, "#contact a[aria-label='GitHub']"),
        "check": "external",
        "expected": "https://github.com/kamanzi-danny",
    },
    {
        "id": "TC-10",
        "what": 'NEGATIVE: click "Services" in the main menu (section does not exist)',
        "locator": (By.CSS_SELECTOR, "#nav a.nav-link[href='#services']"),
        "check": "section",
        "expected": "#services",
        "negative": True,
    },
]
