from typing import Any, Dict, List, Union
from unittest import mock
from unittest.mock import patch, Mock

import pytest

from src.API_class import HeHaAPI


class TestHeHaAPI:

    def test_init(self) -> None:
        api: HeHaAPI = HeHaAPI()
        assert hasattr(api, "base_url")
        assert api.base_url == "https://api.hh.ru/vacancies"

    @patch("requests.get")
    def test_get_vacancies(self, mock_get: Mock) -> None:
        mock_response: mock = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [{"id": 1, "name": "Python Developer"}]
        }
        mock_get.return_value = mock_response

        api: HeHaAPI = HeHaAPI()
        vacancies: List[Dict[str, Any]] = api.get_vacancy("Python")

        assert len(vacancies) == 1
        assert vacancies[0]["name"] == "Python Developer"
        mock_get.assert_called_once()

    @patch("requests.get")
    def test_get_vacancies_error(self, mock_get: Mock) -> None:
        mock_response: Mock = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        api: HeHaAPI = HeHaAPI()
        with pytest.raises(Exception) as exc_info:
            api.get_vacancy("Python")

        assert "Ошибка при запросе: 500" in str(exc_info.value)

    def test_get_vacancies_default_params(self) -> None:
        api: HeHaAPI = HeHaAPI()
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {"items": []}

            api.get_vacancy("Python")

            args: tuple
            kwargs: Dict[str, Any]
            args, kwargs = mock_get.call_args
            params: Dict[str, Union[str, int]] = kwargs["params"]

            assert params["text"] == "Python"
            assert params["search_field"] == "name"
            assert params["per_page"] == 100
            assert params["area"] == 113

    @patch("requests.get")
    def test_get_vacancies_custom_params(self, mock_get: Mock) -> None:
        mock_response: Mock = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": []}
        mock_get.return_value = mock_response

        api: HeHaAPI = HeHaAPI()
        api.get_vacancy("Python", salary=100000, experience="between1And3")
