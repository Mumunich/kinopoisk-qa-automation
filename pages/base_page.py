from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from config.settings import settings


class BasePage:
    """Базовая страница."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, settings.TIMEOUT)

    def find(self, by: By, selector: str):
        """Найти элемент с ожиданием."""
        return self.wait.until(EC.presence_of_element_located((by, selector)))

    def find_visible(self, by: By, selector: str):
        """Найти видимый элемент."""
        return self.wait.until(
            EC.visibility_of_element_located((by, selector))
        )

    def find_clickable(self, by: By, selector: str):
        """Найти кликабельный элемент."""
        return self.wait.until(EC.element_to_be_clickable((by, selector)))
