from typing import Any, Dict, Optional


class Vacancy:
    """
        Класс для представления вакансии.

        Attributes:
            title (str): Название вакансии
            link (str): Ссылка на вакансию
            salary (Dict[str, Any]): Информация о зарплате
            description (str): Описание вакансии
        """

    __slots__ = (
        "title",
        "link",
        "salary",
        "description",
    )
    def __init__(
        self, title: str, link: str, salary: Optional[Dict[str, Any]], description: str
    ) -> None:
        """
                Инициализирует объект вакансии.

                Args:
                    title: Название вакансии
                    link: Ссылка на вакансию
                    salary: Словарь с информацией о зарплате
                    description: Описание вакансии
                """

        self.title: str = title
        self.link: str = link
        self.salary: Dict[str, Any] = self.__validate_salary(salary)
        self.description: str = description

    @staticmethod
    def __validate_salary(salary: Optional[Dict[str, Any]]) -> Dict[str, Any]:

        """
            Валидирует и нормализует данные о зарплате.

            Args:
                salary: Словарь с данными о зарплате или None

            Returns:
                Dict[str, Any]: Нормализованный словарь с данными о зарплате
            """

        if salary is None:
            return {"from": 0, "to": 0, "currency": ""}

        valid_salary = salary.copy()
        valid_salary.setdefault("from", 0)
        valid_salary.setdefault("to", 0)
        valid_salary.setdefault("currency", "")

        if valid_salary["from"] is None:
            valid_salary["from"] = 0
        if valid_salary["to"] is None:
            valid_salary["to"] = 0

        return valid_salary

    def __str__(self) -> str:
        """
                Возвращает строковое представление вакансии для пользователя.

                Returns:
                    str: Форматированная строка с информацией о вакансии
                """
        salary_info = "Зарплата не указана"
        if self.salary:
            from_salary = self.salary.get("from", "?")
            to_salary = self.salary.get("to", "?")
            currency = self.salary.get("currency", "")
            salary_info = f"Зарплата {from_salary} - {to_salary} {currency}".strip()
        return (
            f"{self.title}\n"
            f"{salary_info}\n"
            f"Ссылка: {self.link}\n"
            f"Описание:{self.description[:100]}...\n"
        )

    def __repr__(self) -> str:
        """
                Возвращает официальное строковое представление объекта.

                Returns:
                    str: Строка, которую можно использовать для воссоздания объекта
                """
        return (
            f"Vacancy(title='{self.title}', link='{self.link}', "
            f"salary={self.salary}, description='{self.description[:20]}')"
        )

    def __lt__(self, other: "Vacancy") -> bool:
        """
                Сравнивает вакансии по минимальной зарплате (оператор <).

                Args:
                    other: Другая вакансия для сравнения

                Returns:
                    bool: True если текущая зарплата меньше другой
                """
        return self.get_min_salary() < other.get_min_salary()

    def __le__(self, other: "Vacancy") -> bool:
        """
                Сравнивает вакансии по минимальной зарплате (оператор <=).

                Args:
                    other: Другая вакансия для сравнения

                Returns:
                    bool: True если текущая зарплата меньше или равна другой
                """
        return self.get_min_salary() <= other.get_min_salary()

    def __gt__(self, other: "Vacancy") -> bool:
        """
                Сравнивает вакансии по минимальной зарплате (оператор >).

                Args:
                    other: Другая вакансия для сравнения

                Returns:
                    bool: True если текущая зарплата больше другой
                """
        return self.get_min_salary() > other.get_min_salary()

    def __ge__(self, other: "Vacancy") -> bool:
        """
                Сравнивает вакансии по минимальной зарплате (оператор >=).

                Args:
                    other: Другая вакансия для сравнения

                Returns:
                    bool: True если текущая зарплата больше или равна другой
                """
        return self.get_min_salary() >= other.get_min_salary()

    def __eq__(self, other: object) -> bool:
        """
                Проверяет равенство вакансий по всем атрибутам.

                Args:
                    other: Объект для сравнения

                Returns:
                    bool: True если вакансии полностью идентичны

                Notes:
                    Возвращает NotImplemented если other не является Vacancy
                """
        if not isinstance(other, Vacancy):
            return NotImplemented
        return (
            self.title == other.title
            and self.link == other.link
            and self.salary == other.salary
            and self.description == other.description
        )

    def get_min_salary(self) -> int:
        """
                Возвращает минимальную зарплату вакансии.

                Returns:
                    int: Минимальная зарплата или 0 если не указана
                """
        if not self.salary:
            return 0
        else:
            return max(self.salary.get("from", 0), 0)

    def get_max_salary(self) -> int:
        """
                Возвращает максимальную зарплату вакансии.

                Returns:
                    int: Максимальная зарплата или 0 если не указана
                """
        if not self.salary:
            return 0
        else:
            return max(self.salary.get("to", 0), 0)

    def to_dict(self) -> Dict[str, Any]:
        """
                Преобразует вакансию в словарь.

                Returns:
                    Dict[str, Any]: Словарь с данными вакансии
                """
        return {
            "title": self.title,
            "link": self.link,
            "salary": self.salary,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Vacancy":
        """
                Создает объект Vacancy из словаря данных.

                Args:
                    data: Словарь с данными вакансии

                Returns:
                    Vacancy: Объект вакансии

                Notes:
                    Устанавливает значения по умолчанию для отсутствующих полей
                """
        return cls(
            title=data.get("name", "Без названия"),
            link=data.get("alternate_url", "Ссылка не указана"),
            salary=data.get("salary"),
            description=data.get("snippet", {}).get(
                "requirement", "Описание не указано"
            ),
        )
