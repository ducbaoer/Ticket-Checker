from ticket_checker.scraper import get_event_links, extract_tickets

def test_get_event_links_from_fixture(driver, wait, fixture_url):
    url = fixture_url("ticketio_listing.html")

    links = get_event_links(driver, wait, url)

    assert len(links) == 3
    assert "ticketio_event_available.html" in links[0]
    assert "ticketio_event_sold_out.html" in links[1]
    assert "ticketio_event_mixed.html" in links[2]

def test_extract_available_tickets(driver, wait, fixture_url):
    url = fixture_url("ticketio_event_available.html")

    tickets = extract_tickets(driver, wait, url)

    assert len(tickets) == 2
    assert tickets[0]["status"] == "VERFÜGBAR"
    assert tickets[1]["status"] == "VERFÜGBAR"

def test_extract_sold_out_ticket(driver, wait, fixture_url):
    url = fixture_url("ticketio_event_sold_out.html")

    tickets = extract_tickets(driver, wait, url)

    assert len(tickets) == 1
    assert tickets[0]["status"] == "AUSVERKAUFT"

def test_extract_mixed_tickets(driver, wait, fixture_url):
    url = fixture_url("ticketio_event_mixed.html")

    tickets = extract_tickets(driver, wait, url)

    assert len(tickets) == 3

    assert tickets[0]["status"] == "AUSVERKAUFT"
    assert tickets[1]["status"] == "VERFÜGBAR"
    assert tickets[2]["status"] == "VERFÜGBAR"

def test_full_flow_from_listing(driver, wait, fixture_url):
    listing_url = fixture_url("ticketio_listing.html")

    event_links = get_event_links(driver, wait, listing_url)

    assert len(event_links) == 3

    ticket_available = extract_tickets(driver, wait, event_links[0])

    assert len(ticket_available) == 2
    assert "title" in ticket_available[0]
    assert "price" in ticket_available[0]
    assert "status" in ticket_available[0]