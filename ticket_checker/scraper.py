from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def is_valid_ticket(ticket):
    return (
        ticket.get("title") != "UNKNOWN"
        and ticket.get("price") != "UNKNOWN"
    )

def filter_valid_tickets(tickets):
    return [ticket for ticket in tickets if is_valid_ticket(ticket)]

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def accept_cookies_if_present(driver, wait):
    try:
        button = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[contains(., 'Akzeptieren') or "
                "contains(., 'Alle akzeptieren') or "
                "contains(., 'Zustimmen')]"
            ))
        )
        button.click()
        print("Cookies accepted")

    except TimeoutException:
        pass

def get_event_links(driver, wait, url):
    driver.get(url)
    accept_cookies_if_present(driver, wait)

    if "403" in driver.title or "Forbidden" in driver.page_source:
        raise RuntimeError(f"Access blocked with 403 Forbidden: {url}")

    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
    except TimeoutException:
        print("No links found on page")
        print("URL:", driver.current_url)
        print("Title:", driver.title)
        return []

    links = driver.find_elements(By.TAG_NAME, 'a')
    event_links = []

    for link in links:
        href = link.get_attribute('href')

        spans = link.find_elements(By.TAG_NAME, 'span')

        has_ticket_text = any(
            'tickets' in span.text.lower() for span in spans
        )

        if href and has_ticket_text and href != url:
            if href not in event_links:
                event_links.append(href)

    print(f'Gefundene Events: {len(event_links)}')
    return event_links

def extract_tickets(driver, wait, event_url):
    driver.get(event_url)

    wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr.ticketTypes"))
    )

    wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ticketType-title"))
    )

    wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ticket-price-value"))
    )

    print(f"\nEvent: {event_url}")

    ticket_elements = driver.find_elements(By.CSS_SELECTOR, "tr.ticketTypes")

    tickets = parse_ticket_elements(ticket_elements)
    tickets = filter_valid_tickets(tickets)

    for t in tickets:
        print(f"Ticket: {t['title']} | {t['price']} | {t['status']}")

    return tickets

def has_element(parent, by, selector):
    return len(parent.find_elements(by, selector)) > 0

def parse_ticket_elements(ticket_elements):
    tickets = []

    for el in ticket_elements:
        try:
            title = el.find_element(By.CSS_SELECTOR, ".ticketType-title").text.strip()
        except Exception:
            title = "UNKNOWN"

        try:
            price = el.find_element(By.CSS_SELECTOR, ".ticket-price-value").text.strip()
        except Exception:
            price = "UNKNOWN"

        is_sold_out = has_element(el, By.CSS_SELECTOR, ".ticketTypeSumSoldOut")

        if is_sold_out:
            status = "AUSVERKAUFT"
        elif price != "UNKNOWN" and "Euro" in price:
            status = "VERFÜGBAR"
        else:
            status = "UNBEKANNT"

        tickets.append({
            "title": title,
            "price": price,
            "status": status,
        })

    return tickets