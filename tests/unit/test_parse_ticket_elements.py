from ticket_checker.scraper import parse_ticket_elements

class FakeElement:
    def __init__(self, tag="div", text="", attributes=None, children=None):
        self.tag = tag
        self._text = text
        self._attributes = attributes or {}
        self._children = children or []

    @property
    def text(self):
        parts = []

        if self._text.strip():
            parts.append(self._text.strip())

        for child in self._children:
            child_text = child.text.strip()
            if child_text:
                parts.append(child_text)

        return "\n".join(parts)

    def get_attribute(self, name):
        return self._attributes.get(name)

    def find_element(self, by, selector):
        results = self.find_elements(by, selector)

        if not results:
            raise Exception(f"Element not found: {selector}")

        return results[0]

    def find_elements(self, by, selector):
        results = []

        for child in self._children:
            if child.matches(selector):
                results.append(child)

            results.extend(child.find_elements(by, selector))

        return results

    def matches(self, selector):
        if selector.startswith("."):
            class_name = selector[1:]
            classes = self._attributes.get("class", "").split()
            return class_name in classes

        if selector.startswith("#"):
            element_id = selector[1:]
            return self._attributes.get("id") == element_id

        return self.tag == selector

def make_ticket(title, price, sold_out=False):
    children = [
        FakeElement(
            tag="td",
            children=[
                FakeElement(
                    tag="strong",
                    attributes={"class": "ticketType-title"},
                    text=title,
                )
            ],
        ),
        FakeElement(
            tag="td",
            attributes={"class": "ticketSinglePrice"},
            children=[
                FakeElement(
                    tag="span",
                    attributes={"class": "ticket-price-value"},
                    text=price,
                )
            ],
        ),
    ]

    if sold_out:
        children.append(
            FakeElement(
                tag="td",
                attributes={"class": "ticketTypeSumSoldOut right"},
                children=[
                    FakeElement(
                        tag="span",
                        attributes={"class": "badge badge-important out-badge"},
                        text="Ausverkauft",
                    )
                ],
            )
        )

    return FakeElement(
        tag="tr",
        attributes={"class": "ticketTypes ticketType123"},
        children=children,
    )

def test_parse_ticket_full_logic():
    ticket = make_ticket(
        title="Early Bird",
        price="15,00 Euro",
    )

    result = parse_ticket_elements([ticket])

    parsed = result[0]

    assert parsed == {
        "title": "Early Bird",
        "price": "15,00 Euro",
        "status": "VERFÜGBAR"
    }

def test_ticket_available_status_only():
    ticket = make_ticket(
        title="Regular",
        price="25,00 Euro",
    )

    result = parse_ticket_elements([ticket])

    assert result[0]["status"] == "VERFÜGBAR"

def test_ticket_sold_out_disabled():
    ticket = make_ticket(
        title="Standard",
        price="30,00 Euro",
        sold_out=True
    )

    result = parse_ticket_elements([ticket])

    assert result[0]["status"] == "AUSVERKAUFT"

def test_ticket_sold_out_text():
    ticket = make_ticket(
        title="VIP",
        price="99,00 Euro",
        sold_out=True
    )

    result = parse_ticket_elements([ticket])

    assert result[0]["status"] == "AUSVERKAUFT"

def test_ticket_unknown_status():
    ticket = make_ticket(
        title="Mystery",
        price="??",
    )

    result = parse_ticket_elements([ticket])

    assert result[0]["status"] == "UNBEKANNT"

def test_missing_fields():
    only_title = FakeElement(
        tag="td",
        children=[FakeElement(
            tag="strong",
            attributes={"class": "ticketType-title"},
            text="No Price Ticket")
        ]
    )
    ticket = FakeElement(
        tag="tr",
        attributes={"class": "ticketTypes ticketType123"},
        children=[only_title],
    )

    result = parse_ticket_elements([ticket])

    assert result[0]["title"] == "No Price Ticket"
    assert result[0]["price"] == "UNKNOWN"
    assert result[0]["status"] == "UNBEKANNT"

def test_multiple_tickets():
    ticket_1 = make_ticket(
        title="A",
        price="10 Euro",
    )
    ticket_2 = make_ticket(
        title="B",
        price="20 Euro",
        sold_out=True
    )
    tickets = [ticket_1, ticket_2]

    result = parse_ticket_elements(tickets)

    assert len(result) == 2
    assert result[0]["status"] == "VERFÜGBAR"
    assert result[1]["status"] == "AUSVERKAUFT"