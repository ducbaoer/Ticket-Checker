import pytest

from tests.conftest import e2e_driver
from ticket_checker.config import BASE_URL
from ticket_checker.scraper import get_event_links, extract_tickets


def skip_if_blocked(driver):
    page = driver.page_source.lower()
    title = driver.title.lower()

    if "403" in title or "forbidden" in page:
        pytest.skip("External site blocked Selenium with 403 Forbidden")

@pytest.mark.e2e
def test_start_page_loads_and_event_links_are_found(e2e_driver, e2e_wait):
    event_links = get_event_links(e2e_driver, e2e_wait, BASE_URL)

    skip_if_blocked(e2e_driver)

    assert len(event_links) > 0
    assert all(link.startswith("http") for link in event_links)

@pytest.mark.e2e
def test_event_page_loads_and_ticket_data_is_extracted(e2e_driver, e2e_wait):
    event_links = get_event_links(e2e_driver, e2e_wait, BASE_URL)

    skip_if_blocked(e2e_driver)

    assert len(event_links) > 0

    tickets = extract_tickets(e2e_driver, e2e_wait, event_links[0])

    assert len(tickets) > 0

    first_ticket = tickets[0]

    assert "title" in first_ticket
    assert "price" in first_ticket
    assert "status" in first_ticket

@pytest.mark.e2e
def test_sold_out_tickets_are_detected(e2e_driver, e2e_wait):
    event_links = get_event_links(e2e_driver, e2e_wait, BASE_URL)

    skip_if_blocked(e2e_driver)

    assert len(event_links) > 0

    found_sold_out = False

    for event_link in event_links:
        tickets = extract_tickets(e2e_driver, e2e_wait, event_link)

        if any(ticket["status"] == "AUSVERKAUFT" for ticket in tickets):
            found_sold_out = True
            break

    assert found_sold_out, "No sold-out ticket was found on current live pages"

@pytest.mark.e2e
def test_available_tickets_are_detected(e2e_driver, e2e_wait):
    event_links = get_event_links(e2e_driver, e2e_wait, BASE_URL)

    skip_if_blocked(e2e_driver)

    assert len(event_links) > 0

    found_available = False

    for event_link in event_links:
        tickets = extract_tickets(e2e_driver, e2e_wait, event_link)

        if any(ticket["status"] == "VERFÜGBAR" for ticket in tickets):
            found_available = True
            break

    assert found_available, "No available ticket was found on current live pages"
