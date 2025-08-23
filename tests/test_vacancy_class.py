import unittest
from typing import Optional,Union
from src.vacancy_class import Vacancy


class TestVacancy(unittest.TestCase):

    def setUp(self) -> None:
        self.sample_data = {
            "name": "Python Developer",
            "alternate_url": "http://example.com",
            "salary": {"from": 100000, "to": 150000, "currency": "RUB"},
            "snippet": {"requirement": "Опыт работы с Python"},
        }
        self.vacancy = Vacancy.from_dict(self.sample_data)

    def test_get_min_salary(self) -> None:
        self.assertEqual(self.vacancy.get_min_salary(), 100000)

        vacancy_with_no_salary = Vacancy.from_dict({**self.sample_data, "salary": None})
        self.assertEqual(vacancy_with_no_salary.get_min_salary(), 0)

        vacancy_no_from_salary = Vacancy.from_dict({**self.sample_data, "salary": {"to": 120000}})
        self.assertEqual(vacancy_no_from_salary.get_min_salary(), 0)

        # vacancy_negative_salary = Vacancy.from_dict({**self.sample_data, "salary": {"from": -50000, "to": 120000}})
        # self.assertEqual(vacancy_negative_salary.get_min_salary(), 0)

    def test_get_max_salary(self) -> None:
        self.assertEqual(self.vacancy.get_max_salary(), 150000)

        vacancy_with_no_salary = Vacancy.from_dict({**self.sample_data, "salary": None})
        self.assertEqual(vacancy_with_no_salary.get_max_salary(), 0)

        vacancy_no_to_salary = Vacancy.from_dict({**self.sample_data, "salary": {"from": 100000}})
        self.assertEqual(vacancy_no_to_salary.get_max_salary(), 0)

        # vacancy_negative_salary = Vacancy.from_dict({**self.sample_data, "salary": {"from": 50000, "to": -100000}})
        # self.assertEqual(vacancy_negative_salary.get_max_salary(), 0)

    def test_to_dict(self) -> None:
        expected_dict = {
            "title": "Python Developer",
            "link": "http://example.com",
            # "link": "Ссылка не указана",
            "salary": {"from": 100000, "to": 150000, "currency": "RUB"},
            "description": "Опыт работы с Python",
        }
        self.assertDictEqual(self.vacancy.to_dict(), expected_dict)

        vacancy_with_no_salary = Vacancy.from_dict({**self.sample_data, "salary": None})
        expected_with_no_salary = {
            "title": "Python Developer",
            "link": "http://example.com",
            "salary": {"from": 0, "to": 0, "currency": ""},
            "description": "Опыт работы с Python",
        }
        self.assertDictEqual(vacancy_with_no_salary.to_dict(), expected_with_no_salary)

    def test_from_dict(self) -> None:
        self.assertEqual(self.vacancy.title, "Python Developer")
        self.assertEqual(self.vacancy.link, "http://example.com")
        # self.assertEqual(self.vacancy.link, "Ссылка не указана")
        self.assertEqual(self.vacancy.description, "Опыт работы с Python")
        self.assertEqual(self.vacancy.salary, {"from": 100000, "to": 150000, "currency": "RUB"})

        incomplete_data: dict[str, Optional[Union[str, dict]]] = {
            "name": "Incomplete Python",
            "alternate_url": None,
            "salary": None,
            "snippet": {},
        }

        vacancy_incomplete = Vacancy.from_dict(incomplete_data)
        self.assertEqual(vacancy_incomplete.title, "Incomplete Python")
        self.assertEqual(vacancy_incomplete.link, None)
        self.assertEqual(vacancy_incomplete.description, "Описание не указано")
        self.assertDictEqual(vacancy_incomplete.salary, {"from": 0, "to": 0, "currency": ""})


if __name__ == "__main__":
    unittest.main()