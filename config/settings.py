import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Настройки проекта."""

    # API настройки
    API_URL = os.getenv("KINOPOISK_API_URL", "https://api.kinopoisk.dev/v1.4/")
    API_KEY = os.getenv("KINOPOISK_API_KEY", "")

    # UI настройки
    BASE_URL = os.getenv("KINOPOISK_BASE_URL", "https://www.kinopoisk.ru/")

    # Тестовые данные для API тестов
    WEDNESDAY_ID = 4365427
    EMMA_MYERS_ID = 1875204

    # Тестовые данные для UI тестов
    SEARCH_QUERY_INTERSTELLAR = "Интерстеллар"
    SEARCH_QUERY_WEDNESDAY = "Уэнсдей"  # С ошибкой, чтобы тестировать поиск

    # Таймаут
    TIMEOUT = 20


settings = Settings()
