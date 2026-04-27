from selenium.webdriver.support.ui import WebDriverWait

from ticket_checker.browser import create_driver
from ticket_checker.config import BASE_URL, DEFAULT_WAIT_SECONDS, HEADLESS
from ticket_checker.scraper import get_event_links, extract_tickets


def main():
    driver = create_driver(HEADLESS)
    try:
        wait = WebDriverWait(driver, DEFAULT_WAIT_SECONDS)
        event_links = get_event_links(driver, wait, BASE_URL)

        for event_url in event_links:
            tickets = extract_tickets(driver, wait, event_url)

            for ticket in tickets:
                print(f"{ticket['title']} | {ticket['price']} | {ticket['status']}")

    finally:
        driver.quit()


if __name__ == '__main__':
    main()
