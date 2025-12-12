from selenium.webdriver.common.by import By
from .base_page import BasePage
import time
import allure


class FilmPage(BasePage):
    """Страница фильма."""

    FILM_TITLE = (By.CSS_SELECTOR,
                  'h1[itemprop="name"] span[data-tid="2da92aed"]'
                  )
    RATE_BUTTON = (By.CSS_SELECTOR,
                   '.style_button__Awsrq.'
                   'style_buttonSize32__0wbvn'
                   '.style_buttonPrimary__Qn_9l'
                   )
    RATING_POPUP = (By.CSS_SELECTOR,
                    '.style_ratingPicker__RRKLA'
                    '.ignore-react-onclickoutside'
                    )
    RATING_9 = (By.CSS_SELECTOR,
                '[aria-label="Оценка 9"]'
                '.styles_item__G50X_'
                '.styles_positiveRating__eltjP'
                )
    WATCH_LATER_BUTTON = (By.CSS_SELECTOR, '[title="Буду смотреть"]')

    @allure.step("Получить название фильма")
    def get_title(self) -> str:
        """Получить название фильма."""
        return self.find_visible(*self.FILM_TITLE).text

    @allure.step("Нажать кнопку 'Буду смотреть'")
    def click_watch_later(self) -> bool:
        """Нажать кнопку 'Буду смотреть'."""
        try:
            button = self.find_clickable(*self.WATCH_LATER_BUTTON)
            original_url = self.driver.current_url
            button.click()

            self.wait.until(lambda driver: driver.current_url != original_url)
            return True
        except Exception:
            return False

    @allure.step("Проверить процесс оценки")
    def can_rate_film(self) -> bool:
        """Проверить полный процесс оценки фильма."""
        try:
            # 1. Нажимаем кнопку оценки
            rate_button = self.find_clickable(*self.RATE_BUTTON)
            original_url = self.driver.current_url
            rate_button.click()

            # 2. Ждем попап с оценками
            self.find_visible(*self.RATING_POPUP)

            # 3. ПАУЗА ДЛЯ ДЕМОНСТРАЦИИ (2 секунды)
            time.sleep(2)  # Преподаватель увидит попап

            # 4. Нажимаем оценку 9
            rating_9 = self.find_clickable(*self.RATING_9)
            rating_9.click()

            # 5. Ждем авторизации
            self.wait.until(lambda driver: driver.current_url != original_url)
            return True
        except Exception:
            return False
