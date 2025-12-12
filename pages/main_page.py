from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base_page import BasePage
from config.settings import settings
import allure


class MainPage(BasePage):
    """Главная страница."""

    SEARCH_BOX = (By.CSS_SELECTOR, '[name="kp_query"]')

    @allure.step("Открыть главную страницу")
    def open(self) -> None:
        """Открыть главную страницу."""
        self.driver.get(settings.BASE_URL)
        self.find_visible(*self.SEARCH_BOX)

    @allure.step("Поиск фильма '{query}'")
    def search(self, query: str) -> None:
        """Выполнить поиск."""
        search_box = self.find_clickable(*self.SEARCH_BOX)
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.ENTER)
