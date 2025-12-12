from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
from config.settings import settings
import allure


class SearchPage(BasePage):
    """Страница результатов поиска."""

    WEDNESDAY_LINK = (By.CSS_SELECTOR,
                      'a[data-url="/film/4365427"].js-serp-metrika'
                      )
    RESULTS_CONTAINER = (By.CSS_SELECTOR, '.most_wanted')
    NO_RESULTS = (By.XPATH,
                  '//h2[contains(text(),'
                  '"по вашему запросу ничего не найдено")]'
                  )

    def _wait_for_results(self) -> bool:
        """Внутренний метод: ждать появления результатов."""
        try:
            self.wait.until(
                EC.any_of(
                    EC.presence_of_element_located(self.RESULTS_CONTAINER),
                    EC.presence_of_element_located(self.NO_RESULTS)
                )
            )
            return True
        except Exception:
            return False

    @allure.step("Открыть Уэнздей")
    def open_wednesday(self) -> None:
        """Найти и открыть страницу Уэнздей."""
        if not self._wait_for_results():
            raise Exception("Результаты поиска не загрузились")

        if self.driver.find_elements(*self.NO_RESULTS):
            raise Exception(
                f"По запросу '{settings.SEARCH_QUERY_WEDNESDAY}' "
                f"ничего не найдено"
            )

        link = self.find_clickable(*self.WEDNESDAY_LINK)
        self.driver.execute_script("arguments[0].click();", link)

    @allure.step("Проверить наличие результатов")
    def has_results(self) -> bool:
        """Проверить есть ли результаты поиска."""
        try:
            self._wait_for_results()  # Исправлено здесь тоже
            return not bool(self.driver.find_elements(*self.NO_RESULTS))
        except Exception:
            return False
