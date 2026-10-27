import sys
from datetime import datetime

from includes import constants, functions


def main():
    test_links = {
        constants.ABOUT_TEXT: constants.ABOUT_URL,
        constants.PORTFOLIO_TEXT: constants.PORTFOLIO_URL,
        constants.SERVICES_TEXT: constants.SERVICES_URL,
        constants.CONTACT_TEXT: constants.CONTACT_URL,
    }

    results = {}
    try:
        for link_text, expected_url in test_links.items():
            result = functions.test_click_item(
                constants.TEST_URL,
                expected_url,
                link_text,
            )
            results[link_text] = result
            print(f"Test completed for {link_text}: {result}")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            with open(
                f"logs/LOG_FILE_{timestamp}.txt",
                "w",
                encoding="utf-8",
            ) as log_file:
                log_file.writelines(
                    [
                        f"Test Title: {link_text}\n",
                        f"Test URL: {constants.TEST_URL}\n",
                        f"Target URL: {expected_url}\n",
                        f"Result: {result}\n",
                        f"Time of test: {datetime.now()}\n",
                        "----------------------------------------\n",
                    ]
                )
    finally:
        functions.close_browser()

    passed = sum(1 for r in results.values() if r == "PASS")
    print(f"End of tests: {passed}/{len(test_links)} passed.")
    # Non-zero exit code lets Docker/CI detect a failed run.
    return 0 if passed == len(test_links) else 1


if __name__ == "__main__":
    sys.exit(main())
