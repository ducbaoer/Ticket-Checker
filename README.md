#  Ticket Checker
A simple Python-based tool to automatically check ticket availability on ticket.io event pages using Selenium.
The project extracts event links and ticket information (title, price, availability) and is structured with clean separation between scraping logic, browser setup, and tests.
---
## Features
- Extract event links from ticket listing pages  
- Scrape ticket details (title, price, availability)  
- Detect sold-out vs available tickets  
- Full test setup:
  - Unit tests (no Selenium)
  - Integration tests (with local HTML fixtures)
- Modular architecture (scraper, browser, CLI)
---
## Project Structure
```text
Ticket-Checker/
│
├── ticket_checker/
│   ├── browser.py        # Selenium driver setup
│   ├── scraper.py        # Core scraping logic
│   ├── cli.py            # Entry point
│   └── config.py         # Config (URLs, settings)
│
├── tests/
│   ├── unit/             # Fast logic tests
│   ├── integration/      # Selenium + local HTML
│   ├── fixtures/         # Fake HTML pages
│   └── conftest.py       # Shared pytest fixtures
│
├── main.py               # App entrypoint
├── requirements.txt
└── pytest.ini
```
---
## Installation
Clone the repository:
```bash
git clone https://github.com/ducbaoer/Ticket-Checker.git
cd Ticket-Checker
```
Create a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # macOS/Linux
```
Install dependencies:
```bash
pip install -r requirements.txt
```
---
## Usage
Run the scraper:
```bash
python main.py
```
The script will:

1. Open the configured ticket page
2. Extract event links
3. Visit each event
4. Print ticket availability
### Example Output
```bash
Event: https://example.ticket.io/event

Ticket: Early Bird | 15,00 Euro | VERFÜGBAR
Ticket: Regular | 25,00 Euro | AUSVERKAUFT
```
---
## Testing
Run all tests:
```bash
pytest
```
Run only unit tests:
```bash
pytest tests/unit
```
Run integration tests
```bash
pytest tests/integration
```
---
## Configuration
Edit ticket_checker/config.py:
```bash
BASE_URL = "https://your-ticket-page"
HEADLESS = True
```
---
## Tech Stack
- Python 3
- Selenium
- Pytest
---
## License
MIT License
---
## Tech Stack
@ducbaoer