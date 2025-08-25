from abc import ABC, abstractmethod
from typing import Any, Dict, List

import requests


class API(ABC):
    """
        Абстрактный базовый класс для API работы с вакансиями.

        Provides:
            Базовый интерфейс для получения вакансий из различных источников
        """

    @abstractmethod
    def get_vacancy(self, search_query: str, **kwargs: Any) -> List[Dict[str, Any]]:
        """
                Абстрактный метод для получения вакансий по поисковому запросу.

                Args:
                    search_query: Поисковый запрос для фильтрации вакансий
                    **kwargs: Дополнительные параметры для API

                Returns:
                    List[Dict[str, Any]]: Список словарей с данными вакансий

                Raises:
                    NotImplementedError: Должен быть реализован в дочерних классах
                """
        pass


class HeHaAPI(API):
    """
        Класс для работы с API HeadHunter России.

        Inherits:
            API: Базовый класс для API работы с вакансиями

        Attributes:
            base_url (str): Базовый URL API HeadHunter
        """

    def __init__(self) -> None:
        """
                Инициализирует HeHaAPI с базовым URL API HeadHunter.
                """
        self.base_url = "https://api.hh.ru/vacancies"

    def get_vacancy(self, search_query: str, **kwargs: Any) -> List[Dict[str, Any]]:
        """
                Получает вакансии из API HeadHunter по поисковому запросу.

                Args:
                    search_query: Поисковый запрос для фильтрации вакансий
                    **kwargs: Дополнительные параметры для API (например, salary, experience)

                Returns:
                    List[Dict[str, Any]]: Список словарей с данными вакансий из API

                Raises:
                    Exception: Если произошла ошибка HTTP запроса (status_code != 200)

                Notes:
                    Базовые параметры:
                    - text: Поисковый запрос
                    - search_field: Поле поиска (name - по названию вакансии)
                    - per_page: Количество результатов на страницу (100)
                    - area: Регион поиска (113 - Россия)
                """
        params: Dict[str, Any] = {
            "text": search_query,
            "search_field": "name",
            "per_page": 100,
            "area": 113,
            **kwargs,
        }

        response: requests.Response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            return response.json().get("items", [])
        else:
            raise Exception(f"Ошибка при запросе: {response.status_code}")
