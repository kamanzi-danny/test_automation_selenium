# Portfolio Link Tests – Selenium, Logging & Docker

**Module:** Development Operations (ITLDO801) – Assignment 3: Test Logging and Reporting with Selenium
**Student:** Kamanzi Shikiri Danny

Automated tests for my portfolio at **https://kamanzi-danny.github.io/Portifolio/**.
A headless Chromium browser, driven by Selenium, runs **10 test cases** (menu links, a button,
contact links, an external link, and one negative test). It checks the result of every action, not
just the click. Every run writes its own **structured log file** using Python's `logging` library.

- **Test plan:** [TEST_PLAN.md](TEST_PLAN.md)
- **Log files:** [logs/](logs/), one `test_run_<date>_<time>.log` per run
- **Failure screenshots:** [logs/screenshots/](logs/screenshots/)

## Project structure

```
test_automation_selenium/
├── app.py                  # Runs all tests, writes the run header, results and summary
├── includes/
│   ├── constants.py        # Website URL, wait time, slow-test threshold, folders
│   ├── test_cases.py       # The 10 test cases (TC-01 … TC-10) from the test plan
│   ├── functions.py        # Browser setup and the code that runs and checks one test
│   └── logger.py           # Logging setup: new timestamped log file per run
├── logs/                   # Generated log files (never overwritten)
│   └── screenshots/        # Screenshot saved for every failed test
├── TEST_PLAN.md            # Test plan table
├── requirements.txt        # selenium
├── Dockerfile              # Python 3.12 + Chromium + ChromeDriver (Kigali time zone)
└── docker-compose.yml      # Build and run in one command; logs saved to ./logs
```

## Log format

Every entry: `timestamp | LEVEL | message`

| Entry | Level | Contents |
|---|---|---|
| Run header | INFO | `RUN START`, website, browser + version, operating system, number of tests |
| Test passed | INFO | Test ID, what was tested, expected, actual, `PASS`, duration |
| Test passed but slow (> 3 s) | WARNING | Same as above, plus a "slow" note |
| Test failed | ERROR | Same as above with `FAIL`, plus error message, page URL at the time of failure, screenshot path |
| Run summary | INFO (ERROR if an unexpected failure) | `RUN END`, total, passed, failed, unexpected failures, total duration |

Example:

```
2026-10-27 14:21:00 | INFO    | RUN START | website: https://kamanzi-danny.github.io/Portifolio/index.html | browser: Chrome <version> | OS: Linux ... | tests planned: 10
2026-10-27 14:21:02 | INFO    | TC-01 | Click "About" in the main menu | expected: URL ends #about and section is visible | actual: URL ends #about, section visible | PASS | 1.3 s
2026-10-27 14:21:28 | WARNING | TC-09 | Click the GitHub icon link in the Contact section | expected: browser opens https://github.com/kamanzi-danny | actual: opened https://github.com/kamanzi-danny ... | PASS | 3.5 s | slow: took longer than 3 s
2026-10-27 14:21:38 | ERROR   | TC-10 | NEGATIVE: click "Services" in the main menu ... | actual: element not found within 10 s ... | FAIL | 10.7 s | error: ... | url: ... | screenshot: logs/screenshots/TC-10_fail_....png | note: negative test, failure was expected
2026-10-27 14:21:38 | INFO    | RUN END | total: 10 | passed: 9 | failed: 1 | unexpected failures: 0 | duration: 38.7 s
```

## How it works

- **Waits, not delays:** `WebDriverWait` waits for each element or URL change, up to 10 s. There is no `sleep()`.
- **Checks the result:** section links must change the URL **and** show the section; contact links must have the correct `href`; the GitHub link must open the GitHub profile.
- **Keeps going after a failure:** each test catches its own errors, logs them as `ERROR`, and the run continues.
- **History:** each run creates a new log file, so earlier runs are never overwritten.
- **Exit code:** `0` when all normal tests pass (the negative test failing is expected), `1` if any normal test fails.

## Run with Docker

Start Docker Desktop, then:

```bash
docker compose up --build
```

New log files appear in `logs/`. To run again without rebuilding:

```bash
docker compose up
```

## Run without Docker (optional)

Requires Python 3 and Google Chrome:

```bash
pip install -r requirements.txt
python app.py
```

## Credits

Based on the class lab repo
[kwabenawanziguya/test_automation_selenium](https://github.com/kwabenawanziguya/test_automation_selenium),
extended with a test plan, structured logging, and Docker.
