from typing import Any, List, Set
from unittest.mock import Mock

import pytest

from src.vacancy_class import Vacancy
from src.vacancy_utils import (filter_vacancies, get_vacancies_by_salary,
                               sort_vacancies, get_top_vacancies,
                               print_vacancies)

@pytest.fixture
def sample_vacancies() -> List[Vacancy]:

    mock1 = Mock(spec=Vacancy)
    mock1.title = "Python Developer"
    mock1.description = "Разработчик Python с опытом 3 лет"
    mock1.salary = {"from": 100000, "to": 150000}
    mock1.link = "http://example.com/python"

    mock2 = Mock(spec=Vacancy)
    mock2.title = "Java Developer"
    mock2.description = "Разработчик Java с опытом 5 лет"
    mock2.salary = {"from": 120000, "to": 180000}
    mock2.link = "http://example.com/java"

    mock3 = Mock(spec=Vacancy)
    mock3.title = "DevOps Engineer"
    mock3.description = "DevOps Engineer с опытом 10 лет"
    mock3.salary = None
    mock3.link = "http://example.com/devops"

    mock4 = Mock(spec=Vacancy)
    mock4.title = "Data Scientist"
    mock4.description = "Data Scientist с опытом 2 лет"
    mock4.salary = {"from": 150000, "to": None}
    mock4.link = "http://example.com/data"

    return [mock1, mock2, mock3, mock4]

def test_filter_vacancies(sample_vacancies: List[Vacancy]) -> None:
    result = filter_vacancies(sample_vacancies, [])
    assert result == sample_vacancies

def test_filter_vacancies_with_filter(sample_vacancies: List[Vacancy]) -> None:
    result = filter_vacancies(sample_vacancies, "Python")
    assert len(result) == 1
    assert result[0].title == "Python Developer"

def test_filter_vacancies_with_multiple_words(sample_vacancies: List[Vacancy]) -> None:
    result = filter_vacancies(sample_vacancies, ["developer", "engineer"])
    assert len(result) == 3
    titles: Set[str] = {vacancy.title for vacancy in result}
    assert "Python Developer" in titles
    assert "Java Developer" in titles
    assert "DevOps Engineer" in titles

def test_get_vacancies_by_salary_no_range(sample_vacancies: List[Vacancy]) -> None:
    result = get_vacancies_by_salary(sample_vacancies, "")
    assert result == sample_vacancies

def test_get_vacancies_by_salary_valid_range(sample_vacancies: List[Vacancy]) -> None:
    result = get_vacancies_by_salary(sample_vacancies, "110000-120000")
    assert len(result) == 2
    titles: Set[str] = {vacancy.title for vacancy in result}
    assert "Python Developer" in titles
    assert "Java Developer" in titles
    # assert "Data Scientist" in titles

def test_get_vacancies_by_salary_edge_case(sample_vacancies: List[Vacancy]) -> None:
    result = get_vacancies_by_salary(sample_vacancies, "150000-150000")
    assert len(result) == 3
    titles: Set[str] = {vacancy.title for vacancy in result}
    assert "Python Developer" in titles
    assert "Data Scientist" in titles

def test_get_vacancies_by_salary_invalid_format(sample_vacancies: List[Vacancy], capsys: Any) -> None:
    result = get_vacancies_by_salary(sample_vacancies, "100-200-300")
    captured = capsys.readouterr()
    assert "Неверный формат диапазона зарплат" in captured.out
    assert result == sample_vacancies

def test_sort_vacancies(sample_vacancies: List[Vacancy]) -> None:

    mock_high = Mock(spec=Vacancy)
    mock_high.title = "Senior Python Developer"
    mock_high.description = "Опыт от 5 лет"
    mock_high.salary = {"from": 200000, "to": 250000}
    mock_high.link = "http://example.com/senior"

    vacancies = sample_vacancies + [mock_high]
    sorted_vacancies = sort_vacancies(vacancies)

    assert sorted_vacancies[0].title == "Senior Python Developer"
    assert sorted_vacancies[1].title == "Data Scientist"
    assert sorted_vacancies[2].title == "Java Developer"
    assert sorted_vacancies[3].title == "Python Developer"

def test_get_top_vacancies(sample_vacancies: List[Vacancy]) -> None:
    result = get_top_vacancies(sample_vacancies, 2)
    assert len(result) == 2
    assert result[0].title == "Python Developer"
    assert result[1].title == "Java Developer"

def test_get_top_vacancies_more_than_available(sample_vacancies: List[Vacancy]) -> None:
    result = get_top_vacancies(sample_vacancies, 10)
    assert len(result) == 4

def test_print_vacancies(sample_vacancies: List[Vacancy], capsys: Any) -> None:
    print_vacancies(sample_vacancies[:1])
    captured = capsys.readouterr()
    assert "Python Developer" in captured.out
    assert "100000" in captured.out
    assert "http://example.com/python" in captured.out
    assert "Разработчик Python" in captured.out

def test_print_vacancies_empty(capsys: Any) -> None:
    print_vacancies([])
    captured = capsys.readouterr()
    assert "Нет вакансий для отображения" in captured.out