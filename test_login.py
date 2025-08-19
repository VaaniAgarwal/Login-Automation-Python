import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    service = Service("C:\\chrome-testing\\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.binary_location = "C:\\chrome-testing\\chrome-win64\\chrome.exe"
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=service,options=options)
    driver.implicitly_wait(20)
    yield driver
    time.sleep(5)
    driver.quit()

def test_valid_login(driver):
    driver.get("https://the-internet.herokuapp.com/login")
    driver.find_element(By.ID, "username").send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.flash.success"))
    )
    assert "You logged into a secure area!" in driver.page_source
    time.sleep(5)

def test_invalid_login(driver):
    driver.get("https://the-internet.herokuapp.com/login")
    driver.find_element(By.ID, "username").send_keys("vaani")
    driver.find_element(By.ID, "password").send_keys("Password!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.flash.error"))
    )
    assert "Your username is invalid!" in driver.page_source
    time.sleep(5)