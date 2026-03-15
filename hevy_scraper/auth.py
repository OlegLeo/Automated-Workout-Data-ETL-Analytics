from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from time import sleep
from config import LOGIN_URL, DEFAULT_TIMEOUT

def login(driver: WebDriver, username: str, password: str, timeout: int = DEFAULT_TIMEOUT) -> None:
    """Log into Hevy using the provided credentials."""
    driver.get(LOGIN_URL)
    
    wait = WebDriverWait(driver, timeout)
    
    inputs = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input.sc-2dbec87c-2.qBoLv"))
    )
    
    if len(inputs) < 2:
        raise RuntimeError("Could not find email and password input fields on the login page.")
    
    username_input, password_input = inputs[0], inputs[1]
    
    username_input.clear()
    username_input.send_keys(username)
    
    password_input.clear()
    password_input.send_keys(password)
    
    login_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.sc-a84253f4-0.nGhnG"))
    )
    login_button.click()
    
    sleep(3)
    
