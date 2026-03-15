from pathlib import Path

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def create_driver(download_path: Path) -> webdriver.Firefox:
    """Create and configure a headless Firefox WebDriver with a custom download directory."""
    options = Options()
    options.headless = True
    
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.dir", str(download_path))
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv,application/csv")
    profile.set_preference("pdfjs.disabled", True)

    options.profile = profile
    
    driver = webdriver.Firefox(options=options)
    driver.maximize_window()
    return driver