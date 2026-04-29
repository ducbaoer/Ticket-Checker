import pytest
from pathlib import Path
from selenium.webdriver.support.ui import WebDriverWait

from ticket_checker.browser import create_driver

@pytest.fixture
def driver():
    driver = create_driver(headless=True)
    yield driver
    driver.quit()

@pytest.fixture
def e2e_driver():
    driver = create_driver(headless=False)
    yield driver
    driver.quit()

@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, 15)

@pytest.fixture
def e2e_wait(e2e_driver):
    return WebDriverWait(e2e_driver, 30)

@pytest.fixture
def fixture_url():
    base_dir = Path(__file__).parent / "fixtures"

    def _get_url(name: str):
        return (base_dir / name).resolve().as_uri()

    return _get_url