from abc import ABC, abstractmethod
from typing import Any, Dict, List

import requests


class API(ABC):

    @abstractmethod
    def get_vacancy(self, search_query: str, **kwargs: Any) -> List[Dict[str, Any]]:
        pass


class HeHaAPI(API):

    def __init__(self) -> None:
        self.base_url = "https://api.hh.ru/vacancies"

    def get_vacancy(self, search_query: str, **kwargs: Any) -> List[Dict[str, Any]]:
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
