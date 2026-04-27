from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def get_event_links(driver, wait, url):
    driver.get(url)

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

    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    print(f'\n Event: {event_url}')

    tickets = []

    try:
        # Find Ticket Container
        price_elements = driver.find_elements(By.XPATH, "//*[contains(text(),'Euro')]")
        if not price_elements:
            price_elements = driver.find_elements(By.XPATH, "//*[contains(text(),'€')]")

        ticket_elements = []

        for price_el in price_elements:
            try:
                row = price_el.find_element(By.XPATH, "./ancestor::div[1]")
                ticket_elements.append(row)
            except Exception:
                continue

        tickets = parse_ticket_elements(ticket_elements)

    except Exception as err:
        print(f"Fehler beim Auslesen: {err}")
        tickets = []

    if not tickets:
        print('Tickets nicht gefunden oder ausverkauft.')
    else:
        for t in tickets:
            print(f'Ticket: {t['title']} | {t['price']} | {t['status']}')

    return tickets

def parse_ticket_elements(ticket_elements):
    tickets = []

    for el in ticket_elements:
        text = el.text.strip()

        if not text:
            continue

        lines = text.split("\n")

        title = lines[0].strip() if lines else "UNKNOWN"

        price = "UNKNOWN"
        for line in lines:
            if "Euro" in line or "€" in line:
                price = line.strip()
                break

        lower_text = text.lower()

        if "ausverkauft" in lower_text or "sold out" in lower_text:
            status = "AUSVERKAUFT"
        elif "warenkorb" in lower_text or "cart" in lower_text or price != "UNKNOWN":
            status = "VERFÜGBAR"
        else:
            status = "UNBEKANNT"

        tickets.append({
            "title": title,
            "price": price,
            "status": status,
        })

    return tickets