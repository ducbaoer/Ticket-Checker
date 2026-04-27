from ticket_checker.scraper import parse_ticket_elements

class FakeElement:
    def __init__(self, text="", attributes=None, children=None):
        self._text = text
        self._attributes = attributes or {}
        self._children = children or {}

    @property
    def text(self):
        parts = [self._text.strip()] if self._text else []

        for child in self._children.values():
            child_text = child.text.strip()
            if child_text:
                parts.append(child_text)

        return "\n".join(parts)

    def find_element(self, by, selector):
        if selector in self._children:
            return self._children[selector]
        raise Exception("Element not found")

    def get_attribute(self, name):
        return self._attributes.get(name)

def test_parse_ticket_full_logic():
    ticket = FakeElement(children={
        ".ticket-title": FakeElement(text="Early Bird"),
        ".ticket-price": FakeElement(text="15,00 €"),
        ".ticket-button": FakeElement(text="In den Warenkorb"),
    })

    result = parse_ticket_elements([ticket])

    parsed = result[0]

    assert parsed == {
        "title": "Early Bird",
        "price": "15,00 €",
        "status": "VERFÜGBAR"
    }

def test_ticket_available_status_only():
    ticket = FakeElement(children={
        ".ticket-title": FakeElement(text="Regular"),
        ".ticket-price": FakeElement(text="25,00 €"),
        ".ticket-button": FakeElement(text="In den Warenkorb"),
    })

    result = parse_ticket_elements([ticket])

    assert result[0]["status"] == "VERFÜGBAR"

def test_ticket_sold_out_disabled():
    ticket = FakeElement(children={
        ".ticket-title": FakeElement(text="Standard"),
        ".ticket-price": FakeElement(text="30,00 €"),
        ".ticket-button": FakeElement(
            text="Ausverkauft",
            attributes={"disabled": "true"},
        ),
    })

    result = parse_ticket_elements([ticket])

    assert result[0]["status"] == "AUSVERKAUFT"

def test_ticket_sold_out_text():
    ticket = FakeElement(children={
        ".ticket-title": FakeElement(text="VIP"),
        ".ticket-price": FakeElement(text="99,00 €"),
        ".ticket-button": FakeElement(text="Ausverkauft"),
    })

    result = parse_ticket_elements([ticket])

    assert result[0]["status"] == "AUSVERKAUFT"

def test_ticket_unknown_status():
    ticket = FakeElement(children={
        ".ticket-title": FakeElement(text="Mystery"),
        ".ticket-price": FakeElement(text="??"),
        ".ticket-button": FakeElement(text="Coming soon"),
    })

    result = parse_ticket_elements([ticket])

    assert result[0]["status"] == "UNBEKANNT"

def test_missing_fields():
    ticket = FakeElement(children={
        ".ticket-title": FakeElement(text="No Price Ticket"),
    })

    result = parse_ticket_elements([ticket])

    assert result[0]["title"] == "No Price Ticket"
    assert result[0]["price"] == "UNKNOWN"
    assert result[0]["status"] == "UNBEKANNT"

def test_multiple_tickets():
    tickets = [
        FakeElement(children={
            ".ticket-title": FakeElement(text="A"),
            ".ticket-price": FakeElement(text="10€"),
            ".ticket-button": FakeElement(text="In den Warenkorb"),
        }),
        FakeElement(children={
            ".ticket-title": FakeElement(text="B"),
            ".ticket-price": FakeElement(text="20€"),
            ".ticket-button": FakeElement(text="Ausverkauft"),
        }),
    ]

    result = parse_ticket_elements(tickets)

    assert len(result) == 2
    assert result[0]["status"] == "VERFÜGBAR"
    assert result[1]["status"] == "AUSVERKAUFT"