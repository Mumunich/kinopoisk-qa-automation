import pytest
import allure
import requests
from config.settings import settings


class TestAPI:
    """API тесты из финальной работы."""

    @pytest.mark.api
    @allure.title("Тест: Поиск по id фильма")
    def test_find_movie_by_id(self):
        """Проверить что фильм Wednesday найден по ID."""
        url = f"{settings.API_URL}movie/{settings.WEDNESDAY_ID}"
        headers = {"X-API-KEY": settings.API_KEY, "accept": "application/json"}

        response = requests.get(url, headers=headers, timeout=settings.TIMEOUT)
        movie = response.json()

        assert "Уэнздей" in movie.get("name", ""), \
            f"Фильм не Уэнздей: {movie.get('name')}"

    @pytest.mark.api
    @allure.title("Тест: Поиск по id актёра")
    def test_find_actor_by_id(self):
        """Проверить что актер Эмма Майерс найден по ID."""
        url = f"{settings.API_URL}person/{settings.EMMA_MYERS_ID}"
        headers = {"X-API-KEY": settings.API_KEY, "accept": "application/json"}

        response = requests.get(url, headers=headers, timeout=settings.TIMEOUT)
        actor = response.json()

        assert "Эмма Майерс" in actor.get("name", ""), \
            f"Актер не Эмма Майерс: {actor.get('name')}"

    @pytest.mark.api
    @allure.title("Тест: Поиск фильма по названию")
    def test_find_movie_by_name(self):
        """Проверить что поиск по 'Wednesday' находит сериал."""
        url = f"{settings.API_URL}movie/search"
        params = {"query": "Wednesday", "limit": 10}
        headers = {"X-API-KEY": settings.API_KEY, "accept": "application/json"}

        response = requests.get(
            url, headers=headers, params=params, timeout=settings.TIMEOUT
        )
        data = response.json()
        movies = data.get("docs", [])

        assert any("Уэнздей" in movie.get("name", "") for movie in movies), \
            "Не найдены фильмы с названием 'Уэнздей'"

    @pytest.mark.api
    @allure.title("Тест: Поиск с фальшивым токеном")
    def test_fake_token(self):
        """Проверить ошибку при неверном токене."""
        url = f"{settings.API_URL}movie/{settings.WEDNESDAY_ID}"
        headers = {
            "X-API-KEY": "FAKE_TOKEN_12345",
            "accept": "application/json"
        }

        response = requests.get(url, headers=headers, timeout=settings.TIMEOUT)
        assert response.status_code == 401, \
            f"Доступ не запрещен: {response.status_code}"

    @pytest.mark.api
    @allure.title("Тест: Поиск без токена")
    def test_no_token(self):
        """Проверить ошибку при отсутствии токена."""
        url = f"{settings.API_URL}movie/{settings.WEDNESDAY_ID}"
        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers, timeout=settings.TIMEOUT)
        assert response.status_code == 401, \
            f"Доступ не запрещен: {response.status_code}"

    @pytest.mark.api
    @allure.title("Тест: Пустой поиск")
    def test_empty_search(self):
        """Проверить ошибку при пустом поиске."""
        url = f"{settings.API_URL}movie/"
        headers = {"X-API-KEY": settings.API_KEY, "accept": "application/json"}

        response = requests.get(url, headers=headers, timeout=settings.TIMEOUT)
        assert response.status_code == 400, \
            f"Нет ошибки запроса: {response.status_code}"

    @pytest.mark.api
    @allure.title("Тест: Поиск по некорректному id фильма")
    def test_invalid_movie_id(self):
        """Проверить ошибку при неверном ID фильма."""
        url = f"{settings.API_URL}movie/999999999"
        headers = {"X-API-KEY": settings.API_KEY, "accept": "application/json"}

        response = requests.get(url, headers=headers, timeout=settings.TIMEOUT)
        assert response.status_code == 400, \
            f"Нет ошибки запроса: {response.status_code}"

    @pytest.mark.api
    @allure.title("Тест: Поиск по некорректному id актёра")
    def test_invalid_actor_id(self):
        """Проверить ошибку при неверном ID актера."""
        url = f"{settings.API_URL}person/999999999"
        headers = {"X-API-KEY": settings.API_KEY, "accept": "application/json"}

        response = requests.get(url, headers=headers, timeout=settings.TIMEOUT)
        assert response.status_code == 400, \
            f"Нет ошибки запроса: {response.status_code}"
