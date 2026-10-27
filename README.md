# Portfolio Link Tests (Selenium + Docker)

Automated UI tests for my portfolio site, **https://kamanzi-danny.github.io/Portifolio/**.
A headless Chromium browser, driven by Selenium, opens the page and clicks each
navigation link (About, Projects, Education, Contact), then checks that the browser
lands on the right section. Each result is written to a log file in `logs/`.

The tests run inside a Docker container, so the only thing you need installed is Docker.

## Project structure

```
test_automation_selenium/
├── app.py                # Runs the tests, writes logs, exits 1 if any test fails
├── includes/
│   ├── constants.py      # Site URL and the links to test
│   └── functions.py      # Selenium setup and the click-and-check test
├── logs/                 # One log file per test run
├── requirements.txt      # Python dependencies (selenium)
├── Dockerfile            # Python 3.12 + Chromium + ChromeDriver
├── docker-compose.yml    # Build and run in one command, with logs saved locally
└── .dockerignore
```

## Run with Docker

Build the image:

```bash
docker build -t portfolio-selenium-tests .
```

Run the tests and keep the logs on your computer:

```bash
docker run --rm --shm-size=1g -v "$(pwd)/logs:/app/logs" portfolio-selenium-tests
```

On Windows PowerShell, use `${PWD}` instead of `$(pwd)`.

Or do both steps with Docker Compose:

```bash
docker compose up --build
```

## Expected output

```
Link test for About passed: https://kamanzi-danny.github.io/Portifolio/index.html#about
Test completed for About: PASS
...
End of tests: 4/4 passed.
```

Example log file (`logs/LOG_FILE_<timestamp>.txt`):

```
Test Title: About
Test URL: https://kamanzi-danny.github.io/Portifolio/index.html
Target URL: https://kamanzi-danny.github.io/Portifolio/index.html#about
Result: PASS
Time of test: 2026-10-26 20:42:05.073242
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
adapted to test my own portfolio and packaged with Docker.
