import os
from typing import Any, Dict, List

from src.API_class import HeHaAPI
from src.save_json_file import CsvSaver, JsonSaver, TxtSaver
from src.vacancy_class import Vacancy
from src.vacancy_utils import (
    filter_vacancies,
    get_top_vacancies,
    get_vacancies_by_salary,
    print_vacancies,
    sort_vacancies,
)


def main() -> None:
    """
        Основная функция для запуска приложения по поиску вакансий.

        Notes:
            Вызывает функцию взаимодействия с пользователем
        """
    user_interaction()


def save_vacancies(vacancies: List[Vacancy], dir_path: str = "data") -> None:
    """
        Сохраняет вакансии в файлы различных форматов в указанную директорию.

        Args:
            vacancies: Список объектов Vacancy для сохранения
            dir_path: Путь к директории для сохранения (по умолчанию: "data")

        Notes:
            Сохраняет данные в трех форматах: JSON, CSV и TXT
            Создает директорию, если она не существует
        """
    os.makedirs(dir_path, exist_ok=True)

    vacancies_data = [vacancy.to_dict() for vacancy in vacancies]

    json_path = os.path.join(dir_path, "vacancies.json")
    json_saver = JsonSaver(json_path)
    json_saver.save_vacancies(vacancies_data)
    print(f"Данные сохранены в файл JSON {os.path.abspath(json_path)}")

    csv_path = os.path.join(dir_path, "vacancies.csv")
    csv_saver = CsvSaver(csv_path)
    csv_saver.save_vacancies(vacancies_data)
    print(f"Данные сохранены в файл CSV {os.path.abspath(csv_path)}")

    txt_path = os.path.join(dir_path, "vacancies.txt")
    txt_saver = TxtSaver(txt_path)
    txt_saver.save_vacancies(vacancies_data)
    print(f"Данные сохранены в файл TXT {os.path.abspath(txt_path)}")


def user_interaction() -> None:
    """
        Осуществляет взаимодействие с пользователем и обработку вакансий.

        Steps:
            1. Запрашивает параметры поиска у пользователя
            2. Получает вакансии из API HeadHunter
            3. Фильтрует и сортирует вакансии
            4. Выводит результаты
            5. Сохраняет результаты в файлы

        Raises:
            ValueError: Если введено некорректное число для top_n
            Exception: Если произошла ошибка при запросе к API
        """
    search_query: str = input("Введите запрос для поиска вакансий: ")
    top_n: int = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words: List[str] = input(
        "Введите ключевые слова для фильтрации вакансий: "
    ).split()
    salary_range: str = input("Введите диапазон зарплат ('min-max'): ")

    hh_api: HeHaAPI = HeHaAPI()
    vacancies_data: List[Dict[str, Any]] = hh_api.get_vacancy(search_query)

    vacancies: List[Vacancy] = [
        Vacancy.from_dict(vacancy) for vacancy in vacancies_data
    ]

    filtred: List[Vacancy] = filter_vacancies(vacancies, filter_words)

    ranged: List[Vacancy] = get_vacancies_by_salary(filtred, salary_range)

    sorted_vacancies: List[Vacancy] = sort_vacancies(ranged)

    top_vacancies: List[Vacancy] = get_top_vacancies(sorted_vacancies, top_n)

    print("\nРезультаты поиска:")
    print("=" * 50)
    print_vacancies(top_vacancies)

    save_vacancies(top_vacancies)


if __name__ == "__main__":
    """
        Точка входа в приложение.

        Notes:
            Запускает основную функцию приложения при прямом выполнении файла
        """
    main()
