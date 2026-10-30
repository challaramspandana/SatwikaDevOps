import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(options=options)
    browser.get("http://127.0.0.1:5000")

    yield browser

    browser.quit()


def test_homepage(driver):
    assert "PetCare" in driver.title


def test_available_pets(driver):
    assert "Available Pets" in driver.page_source
    assert "Bruno" in driver.page_source


def test_rescue_form(driver):
    form = driver.find_element(By.ID, "rescue-form")
    assert form.is_displayed()


def test_pet_cards(driver):
    pets = driver.find_elements(By.CLASS_NAME, "pet-card")
    assert len(pets) > 0
