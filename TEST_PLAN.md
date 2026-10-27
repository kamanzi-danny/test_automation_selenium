# Test Plan – Portfolio Link Tests

**Module:** Development Operations (ITLDO801) – Assignment 3
**Student:** Kamanzi Shikiri Danny
**Website under test:** https://kamanzi-danny.github.io/Portifolio/index.html
**Browser:** Headless Chromium (inside Docker), window 1366 × 900
**Script:** `app.py` (test cases are defined in `includes/test_cases.py`)

Every test starts by opening the home page. Each test ID below appears in the log files in `logs/`.

| Test ID | What is tested | Steps | Expected result |
|---|---|---|---|
| TC-01 | "About" link in the main menu | 1. Open the home page. 2. Wait for the menu link `#about`. 3. Click it. | URL ends with `#about` and the About section is visible. |
| TC-02 | "Projects" link in the main menu | 1. Open the home page. 2. Wait for the menu link `#projects`. 3. Click it. | URL ends with `#projects` and the Projects section is visible. |
| TC-03 | "Education" link in the main menu | 1. Open the home page. 2. Wait for the menu link `#education`. 3. Click it. | URL ends with `#education` and the Education section is visible. |
| TC-04 | "Certifications" link in the main menu | 1. Open the home page. 2. Wait for the menu link `#certifications`. 3. Click it. | URL ends with `#certifications` and the Certifications section is visible. |
| TC-05 | "Contact" link in the main menu | 1. Open the home page. 2. Wait for the menu link `#contact`. 3. Click it. | URL ends with `#contact` and the Contact section is visible. |
| TC-06 | "View projects" button at the top of the page | 1. Open the home page. 2. Wait for the "View projects" button. 3. Click it. | URL ends with `#projects` and the Projects section is visible. |
| TC-07 | Email link in the Contact section | 1. Open the home page. 2. Find the `mailto:` link in Contact. 3. Read its `href`. | `href` is `mailto:kamanzidanny5@gmail.com`. |
| TC-08 | LinkedIn icon link in the Contact section | 1. Open the home page. 2. Find the LinkedIn icon link. 3. Read its `href`. | `href` is `https://www.linkedin.com/in/kamanzi-s-252880196/`. |
| TC-09 | GitHub icon link in the Contact section (external link) | 1. Open the home page. 2. Scroll to the GitHub icon. 3. Click it. | Browser opens `https://github.com/kamanzi-danny`. |
| TC-10 | **Negative test:** "Services" link in the main menu | 1. Open the home page. 2. Wait up to 10 s for a menu link `#services`. | The site has **no** Services section, so the link is not found. The test must be recorded as **FAIL** and logged as **ERROR** with the error message, page URL and a screenshot. |

## How results are judged

- **PASS:** the actual result matches the expected result.
- **FAIL:** anything else (element not found, wrong URL, section not visible, wrong `href`). The failure is logged as `ERROR` and the script carries on with the next test.
- **WARNING:** the test passed but took longer than 3 seconds (a slow page or link).
- **Negative test (TC-10):** a FAIL here is the expected outcome. It proves that failures are caught and logged. The run summary counts it under "failed", but not under "unexpected failures".

## Notes on the TC-07 and TC-08 checks

- **TC-07:** A `mailto:` link opens an email app, not a web page, so the test checks the link's address (`href`) instead of clicking it.
- **TC-08:** LinkedIn blocks automated browsers with a sign-in wall, so the test checks the link's address (`href`) instead of clicking it.
