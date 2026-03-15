from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver

from config import EXPORT_URL, DEFAULT_TIMEOUT

def navigate_to_export_page(driver: WebDriver, timeout: int = DEFAULT_TIMEOUT) -> None:
    """Navigate to the Hevy export settings page."""
    driver.get(EXPORT_URL)
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    
    
def trigger_export(driver: WebDriver, timeout: int = DEFAULT_TIMEOUT) -> None:
    """Click the export button to download the CSV."""
    wait = WebDriverWait(driver, timeout)

    export_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.sc-a84253f4-0.jYMVBH"))
    )
    export_button.click()

