import os
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

WAKE_BUTTON_XPATH = "//button[contains(text(),'Yes, get this app back up')]"
STREAMLIT_URL = os.environ.get("STREAMLIT_APP_URL", "https://chatbotskripsi.streamlit.app/")


def build_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=options)  # Selenium Manager resolves chromedriver itself


def wake_app(driver: webdriver.Chrome, url: str, timeout: int = 15) -> bool:
    """Click the wake-up button if present. Returns False only if the click didn't take effect."""
    driver.get(url)
    print(f"Opened {url}")
    wait = WebDriverWait(driver, timeout)

    try:
        button = wait.until(EC.element_to_be_clickable((By.XPATH, WAKE_BUTTON_XPATH)))
    except TimeoutException:
        print("No wake-up button found. Assuming app is already awake.")
        return True

    print("Wake-up button found. Clicking...")
    button.click()

    try:
        wait.until(EC.invisibility_of_element_located((By.XPATH, WAKE_BUTTON_XPATH)))
        print("Button clicked and disappeared (app should be waking up).")
        return True
    except TimeoutException:
        print("Button was clicked but did NOT disappear (possible failure).")
        return False


def main() -> None:
    driver = build_driver()
    try:
        awake = wake_app(driver, STREAMLIT_URL)
    finally:
        driver.quit()
        print("Script finished.")
    if not awake:
        sys.exit(1)


if __name__ == "__main__":
    main()
