from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# configuration
URL = 'https://blitzclub.ticket.io/?land=de'
# URL = 'https://blitzclub.ticket.io/cKczvTSi/?land=de'

# path to chromedriver
CHROMEDRIVER_PATH = 'chromedriver-win64/chromedriver.exe'

# Browser setup
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service)

wait = WebDriverWait(driver, 15)

def get_event_links():
    driver.get(URL)

    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'a')))

    links = driver.find_elements(By.TAG_NAME, 'a')
    event_links = []

    for link in links:
        href = link.get_attribute('href')

        spans = link.find_elements(By.TAG_NAME, 'span')

        has_ticket_text = any(
            'tickets' in span.text.lower() for span in spans
        )

        if href and has_ticket_text and href != URL:
            if href not in event_links:
                event_links.append(href)

    print(f'Gefundene Events: {len(event_links)}')
    return event_links

def extract_tickets(event_url):
    driver.get(event_url)

    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    print(f'\n Event: {event_url}')

    tickets = []

    try:
        # Find Ticket Container
        price_elements = driver.find_elements(By.XPATH, "//*[contains(text(),'Euro')]")

        for price_el in price_elements:
            try:
                row = price_el.find_element(By.XPATH, "./ancestor::div[1]")

                text = row.text.strip()

                if not text:
                    continue

                lines = text.split('\n')
                title = lines[0]

                price = price_el.text.strip()

                lower_text = text.lower()

                if 'ausverkauft' in lower_text or 'sold out' in lower_text:
                    status = 'AUSVERKAUFT'
                else:
                    status = 'VERFÜGBAR'

                if title != 'Unbekannt' or price != 'Kein Preis':
                    ticket = {
                        'title': title,
                        'price': price,
                        'status': status
                    }
                    tickets.append(ticket)
            except:
                continue

    except Exception as err:
        print(f'Fehler beim Auslesen: {err}')

    if not tickets:
        print('Tickets nicht gefunden oder ausverkauft.')
    else:
        for t in tickets:
            print(f'Ticket: {t['title']} | {t['price']} | {t['status']}')

    return tickets

def check_tickets():
    driver.get(URL)

    try:
        # Wait until page is loaded
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # Check for sold out tickets
        page_text = driver.page_source.lower()

        if 'ausverkauft' in page_text or 'sold out' in page_text:
            print('Tickets aktuell nichtverfügbar.')
            return False

        # Search for Dropdown
        selects = driver.find_elements(By.TAG_NAME, 'select')

        if len(selects) > 0:
            print('Es sind Tickets verfügbar.')
            return True

    except NoSuchElementException:
        print('Tickets werden nicht verkauft')

    print('Keine Ticket Auswahl gefunden.')
    return False

def main():
    try:
        event_links = get_event_links()

        all_data = {}

        for link in event_links:
            tickets = extract_tickets(link)
            all_data[link] = tickets

    finally:
        driver.quit()


if __name__ == '__main__':
    main()
