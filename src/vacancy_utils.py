from typing import List

from src.vacancy_class import Vacancy

# def filter_vacancies(vacancies: List[Vacancy], filter_words: List[str]) -> List[Vacancy]:
#     if not filter_words:
#         return vacancies
#
#     if isinstance(filter_words, str):
#         filter_words = [filter_words]
#
#     filtered = []
#     for vacancy in vacancies:
#         for word in filter_words:
#             if (word.lower() in vacancy.title.lower()) or (word.lower() in vacancy.description.lower()):
#                 filtered.append(vacancy)
#                 break
#     return filtered


def filter_vacancies(
    vacancies: List[Vacancy], filter_words: List[str]
) -> List[Vacancy]:
    """
        Фильтрует вакансии по ключевым словам в названии или описании.

        Args:
            vacancies: Список вакансий для фильтрации
            filter_words: Список ключевых слов для поиска (может быть строкой)

        Returns:
            List[Vacancy]: Отфильтрованный список вакансий

        Notes:
            - Если filter_words пуст, возвращает все вакансии
            - Если переданная строка, преобразует её в список
            - Игнорирует регистр при поиске
            - Защищена от None значений в title и description
        """
    if not filter_words:
        return vacancies

    if isinstance(filter_words, str):
        filter_words = [filter_words]

    filtered = []
    for vacancy in vacancies:
        for word in filter_words:
            title = vacancy.title or ""
            description = vacancy.description or ""

            if (word.lower() in title.lower()) or (word.lower() in description.lower()):
                filtered.append(vacancy)
                break
    return filtered


# def get_vacancies_by_salary(vacancies: List[Vacancy], salary_range: str) -> List[Vacancy]:
#     if not salary_range:
#         return vacancies
#
#     try:
#         salary_from, salary_to = map(int, salary_range.split('-'))
#     except ValueError:
#         print('Неверный формат диапазона зарплат. Используйте формат "min-max".')
#         return vacancies
#
#     filtered = []
#     for vacancy in vacancies:
#         if vacancy.salary is None:
#             continue
#
#         if vacancy.salary and 'from' in vacancy.salary and 'to' in vacancy.salary:
#             salary_from_vacancy = vacancy.salary['from'] or 0
#             salary_to_vacancy = vacancy.salary['to'] or float('inf')
#             if (salary_from <= salary_from_vacancy <= salary_to) or (salary_from <= salary_to_vacancy <= salary_to):
#                 filtered.append(vacancy)
#     return filtered


def get_vacancies_by_salary(
    vacancies: List[Vacancy], salary_range: str
) -> List[Vacancy]:
    """
        Фильтрует вакансии по диапазону зарплат.

        Args:
            vacancies: Список вакансий для фильтрации
            salary_range: Диапазон зарплат в формате 'min-max'

        Returns:
            List[Vacancy]: Отфильтрованный список вакансий

        Raises:
            ValueError: Если формат salary_range некорректный

        Notes:
            - Если salary_range пуст, возвращает все вакансии
            - Игнорирует вакансии без информации о зарплате
            - Проверяет пересечение диапазонов зарплат
        """
    if not salary_range:
        return vacancies

    try:
        salary_from, salary_to = map(int, salary_range.split("-"))
    except ValueError:
        print('Неверный формат диапазона зарплат. Используйте формат "min-max".')
        return vacancies

    filtered = []
    for vacancy in vacancies:
        if vacancy.salary is None:
            continue

        vac_salary_from = vacancy.salary.get("from")
        vac_salary_to = vacancy.salary.get("to")

        if vac_salary_from is None and vac_salary_to is None:
            continue

        if vac_salary_from is not None and salary_from <= vac_salary_from <= salary_to:
            filtered.append(vacancy)
        elif vac_salary_to is not None and salary_from <= vac_salary_to <= salary_to:
            filtered.append(vacancy)
        elif vac_salary_from is not None and vac_salary_to is not None:
            if not (vac_salary_to < salary_from or vac_salary_from > salary_to):
                filtered.append(vacancy)

    return filtered


# def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
#     return sorted(
#         vacancies,
#         key=lambda x: (
#             x.salary['from']
#             if x.salary and 'from' in x.salary and x.salary['from'] is not None
#             else float('-inf')
#         ),
#         reverse=True,
#     )


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """
        Сортирует вакансии по минимальной зарплате в порядке убывания.

        Args:
            vacancies: Список вакансий для сортировки

        Returns:
            List[Vacancy]: Отсортированный список вакансий

        Notes:
            - Вакансии без зарплаты считаются с зарплатой 0
            - Сортировка по убыванию (от большей зарплаты к меньшей)
        """
    return sorted(
        vacancies,
        key=lambda x: (x.salary.get("from", 0) if x.salary else 0),
        reverse=True,
    )


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """
        Возвращает топ N вакансий из списка.

        Args:
            vacancies: Список вакансий
            top_n: Количество вакансий для возврата

        Returns:
            List[Vacancy]: Список из первых top_n вакансий

        Notes:
            - Если top_n больше длины списка, возвращает все вакансии
            - Если vacancies пуст, возвращает пустой список
        """
    return vacancies[:top_n]


# def print_vacancies(vacancies: List[Vacancy]) -> None:
#     if not vacancies:
#         print('Нет вакансий для отображения')
#         return
#
#     for i, vacancy in enumerate(vacancies, 1):
#         print(f'\n{i}. {vacancy.title}')
#         print(f'Зарплата: {vacancy.salary or 'не указана'}')
#         print(f'Ссылка: {vacancy.link}')
#         print(f'Описание: {vacancy.description[:200]}...')
#         print('-' * 50)


def print_vacancies(vacancies: List[Vacancy]) -> None:
    """
        Выводит отформатированную информацию о вакансиях.

        Args:
            vacancies: Список вакансий для отображения

        Notes:
            - Если список пуст, выводит сообщение об отсутствии вакансий
            - Форматирует зарплату в читаемый вид
            - Обрезает описание до 200 символов
            - Защищена от None значений в описании
        """
    if not vacancies:
        print("Нет вакансий для отображения")
        return

    for i, vacancy in enumerate(vacancies, 1):
        print(f"\n{i}. {vacancy.title}")
        salary_str = "не указана"
        if vacancy.salary:
            from_salary = vacancy.salary.get("from", "не указано")
            to_salary = vacancy.salary.get("to", "не указано")
            salary_str = f"{from_salary} - {to_salary}"
        print(f"Зарплата: {salary_str}")
        print(f"Ссылка: {vacancy.link}")
        description = vacancy.description or "Описание отсутствует"
        print(f"Описание: {description[:200]}...")
        print("-" * 50)
