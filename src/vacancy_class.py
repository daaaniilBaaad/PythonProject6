from typing import Any, Dict, Optional


class Vacancy:
    def __init__(
        self, title: str, link: str, salary: Optional[Dict[str, Any]], description: str
    ) -> None:

        self.title: str = title
        self.link: str = link
        self.salary: Dict[str, Any] = self.validate_salary(salary)
        self.description: str = description

    @staticmethod
    def validate_salary(salary: Optional[Dict[str, Any]]) -> Dict[str, Any]:
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
        return (
            f"Vacancy(title='{self.title}', link='{self.link}', "
            f"salary={self.salary}, description='{self.description[:20]}')"
        )

    def __lt__(self, other: "Vacancy") -> bool:
        return self.get_min_salary() < other.get_min_salary()

    def __le__(self, other: "Vacancy") -> bool:
        return self.get_min_salary() <= other.get_min_salary()

    def __gt__(self, other: "Vacancy") -> bool:
        return self.get_min_salary() > other.get_min_salary()

    def __ge__(self, other: "Vacancy") -> bool:
        return self.get_min_salary() >= other.get_min_salary()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return (
            self.title == other.title
            and self.link == other.link
            and self.salary == other.salary
            and self.description == other.description
        )

    def get_min_salary(self) -> int:
        if not self.salary:
            return 0
        else:
            return max(self.salary.get("from", 0), 0)

    def get_max_salary(self) -> int:
        if not self.salary:
            return 0
        else:
            return max(self.salary.get("to", 0), 0)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "link": self.link,
            "salary": self.salary,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Vacancy":
        return cls(
            title=data.get("name", "Без названия"),
            link=data.get("alternate_url", "Ссылка не указана"),
            salary=data.get("salary"),
            description=data.get("snippet", {}).get(
                "requirement", "Описание не указано"
            ),
        )
