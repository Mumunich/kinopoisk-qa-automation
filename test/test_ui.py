import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pages.main_page import MainPage
from pages.search_page import SearchPage
from pages.film_page import FilmPage
from config.settings import settings


@pytest.fixture(scope="function")
def driver():
    """Создать драйвер для теста."""
    service = Service(ChromeDriverManager().install())
    options = Options()
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def pages(driver):
    """Инициализировать страницы."""
    return {
        'main': MainPage(driver),
        'search': SearchPage(driver),
        'film': FilmPage(driver)
    }


class TestUI:
    """UI тесты."""

    @pytest.mark.ui
    @pytest.mark.smoke
    @allure.title("Тест: Поиск фильма по названию")
    def test_search_movie(self, driver, pages):
        """Проверить что поиск 'Интерстеллар' работает (Smoke тест 39)."""
        pages['main'].open()
        pages['main'].search(settings.SEARCH_QUERY_INTERSTELLAR)
        assert pages['search'].has_results()

    @pytest.mark.ui
    @pytest.mark.smoke
    @allure.title("Тест: Открытие карточки сериала Уэнздей")
    def test_open_movie_card(self, driver, pages):
        """Проверить что можно открыть карточку Уэнздей."""
        pages['main'].open()
        pages['main'].search(settings.SEARCH_QUERY_WEDNESDAY)
        pages['search'].open_wednesday()

        title = pages['film'].get_title()
        assert title and (
            "уэнздей" in title.lower() or "wednesday" in title.lower()
        )

    @pytest.mark.ui
    @allure.title("Тест: Проверка элементов главной страницы")
    def test_main_page_elements(self, driver, pages):
        """Проверить основные элементы главной страницы."""
        pages['main'].open()

        search_box = pages['main'].find_visible(*pages['main'].SEARCH_BOX)
        assert search_box.is_displayed()

    @pytest.mark.ui
    @allure.title("Тест: Проверка кнопки 'Буду смотреть'")
    def test_watch_later_button(self, driver, pages):
        """Проверить кнопку 'Буду смотреть'."""
        pages['main'].open()
        pages['main'].search(settings.SEARCH_QUERY_WEDNESDAY)
        pages['search'].open_wednesday()

        assert pages['film'].click_watch_later()

    @pytest.mark.ui
    @allure.title("Тест: Голосование за фильм")
    def test_film_rating_process(self, driver, pages):
        """Проверить процесс оценки фильма."""
        pages['main'].open()
        pages['main'].search(settings.SEARCH_QUERY_WEDNESDAY)
        pages['search'].open_wednesday()

        assert pages['film'].can_rate_film()
