"""Portfolio link tests with structured logging (ITLDO801 - Assignment 3).

Each run writes one log file in logs/ with:
  - a RUN START header (date, website, browser + version, operating system)
  - one entry per test (ID, what, expected, actual, status, duration)
  - a RUN END summary (total, passed, failed, duration)
"""

import platform
import sys
import time

from includes import constants
from includes.functions import create_driver, run_test
from includes.logger import setup_logger
from includes.test_cases import TEST_CASES


def main():
    logger, log_path = setup_logger()
    run_start = time.perf_counter()

    driver = create_driver()
    caps = driver.capabilities
    browser = f"{caps.get('browserName', 'chrome').title()} {caps.get('browserVersion', '?')}"
    operating_system = f"{platform.system()} {platform.release()} ({platform.machine()})"

    # ---- Run header ----
    logger.info(
        "RUN START | website: %s | browser: %s | OS: %s | tests planned: %d",
        constants.TEST_URL, browser, operating_system, len(TEST_CASES),
    )

    results = []
    try:
        for test in TEST_CASES:
            result = run_test(driver, test)
            results.append(result)
            log_result(logger, result)
    finally:
        driver.quit()

    # ---- Run summary ----
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = len(results) - passed
    unexpected = [r["id"] for r in results if r["status"] == "FAIL" and not r["negative"]]
    total_time = time.perf_counter() - run_start

    summary = (
        f"RUN END | total: {len(results)} | passed: {passed} | failed: {failed} "
        f"| unexpected failures: {len(unexpected)}"
        f"{' (' + ', '.join(unexpected) + ')' if unexpected else ''} "
        f"| duration: {total_time:.1f} s | log file: {log_path}"
    )
    if unexpected:
        logger.error(summary)
    else:
        logger.info(summary)

    # Exit code 1 only if a normal (non-negative) test failed.
    return 1 if unexpected else 0


def log_result(logger, r):
    """Write one structured log entry for a test result."""
    entry = (
        f"{r['id']} | {r['what']} | expected: {r['expected']} "
        f"| actual: {r['actual']} | {r['status']} | {r['duration']:.1f} s"
    )

    if r["status"] == "FAIL":
        # Failures: ERROR, with the error message, URL and screenshot.
        details = f" | error: {r['error']} | url: {r['url']}"
        if r["screenshot"]:
            details += f" | screenshot: {r['screenshot']}"
        if r["negative"]:
            details += " | note: negative test, failure was expected"
        logger.error(entry + details)
    elif r["duration"] > constants.SLOW_TEST_SECONDS:
        # Passed, but slower than expected: WARNING.
        logger.warning(
            entry + f" | slow: took longer than {constants.SLOW_TEST_SECONDS:.0f} s"
        )
    else:
        logger.info(entry)


if __name__ == "__main__":
    sys.exit(main())
