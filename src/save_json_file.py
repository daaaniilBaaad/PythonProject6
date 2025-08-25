import csv
import json
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, cast


class FileSaver(ABC):
    """
        Абстрактный базовый класс для сохранения и загрузки вакансий в файлы.

        Provides:
            Базовый интерфейс для работы с файлами различных форматов
        """
    def __init__(self, filename: str) -> None:
        """
                Инициализирует FileSaver с указанным именем файла.

                Args:
                    filename: Имя файла для работы с вакансиями
                """
        self._filename = filename

    @abstractmethod
    def load_vacancies(self) -> List[Dict[str, Any]]:
        """
                Загружает вакансии из файла.

                Returns:
                    List[Dict[str, Any]]: Список словарей с данными вакансий

                Raises:
                    FileNotFoundError: Если файл не существует
                    JSONDecodeError: Для JSON файлов при невалидном формате
                """
        pass

    @abstractmethod
    def save_vacancies(self, data: List[Dict[str, Any]]) -> None:
        """
                Сохраняет вакансии в файл.

                Args:
                    data: Список словарей с данными вакансий для сохранения
                """
        pass

    def add_vacancy(self, vacancy: Dict[str, Any]) -> None:
        """
                Добавляет вакансию в файл, если её там нет.

                Args:
                    vacancy: Словарь с данными вакансии для добавления
                """
        data = self.load_vacancies()
        if vacancy not in data:
            data.append(vacancy)
            self.save_vacancies(data)

    def delete_vacancy(self, vacancy: Dict[str, Any]) -> None:
        """
                Удаляет вакансию из файла, если она существует.

                Args:
                    vacancy: Словарь с данными вакансии для удаления
                """
        data = self.load_vacancies()
        if vacancy in data:
            data.remove(vacancy)
            self.save_vacancies(data)


class JsonSaver(FileSaver):
    """
        Класс для сохранения и загрузки вакансий в формате JSON.

        Inherits:
            FileSaver: Базовый класс для работы с файлами
        """
    def __init__(self, filename: str = "vacancies.json") -> None:
        """
                Инициализирует JsonSaver с именем файла по умолчанию.

                Args:
                    filename: Имя JSON файла (по умолчанию: vacancies.json)
                """
        super().__init__(filename)

    def load_vacancies(self) -> List[Dict[str, Any]]:
        """
                Загружает вакансии из JSON файла.

                Returns:
                    List[Dict[str, Any]]: Список словарей с данными вакансий

                Notes:
                    Если файл не существует, возвращает пустой список
                """
        if not os.path.exists(self._filename):
            return []
        with open(self._filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            return cast(List[Dict[str, Any]], data)

    def save_vacancies(self, data: List[Dict[str, Any]]) -> None:
        """
                Сохраняет вакансии в JSON файл с красивым форматированием.

                Args:
                    data: Список словарей с данными вакансий для сохранения

                Notes:
                    Использует отступ 4 пробела и обеспечивает корректную кодировку UTF-8
                """
        with open(self._filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


class CsvSaver(FileSaver):
    """
        Класс для сохранения и загрузки вакансий в формате CSV.

        Inherits:
            FileSaver: Базовый класс для работы с файлами
        """
    def __init__(self, filename: str = "vacancies.csv") -> None:
        """
                Инициализирует CsvSaver с именем файла по умолчанию.

                Args:
                    filename: Имя CSV файла (по умолчанию: vacancies.csv)
                """
        super().__init__(filename)

    def load_vacancies(self) -> List[Dict[str, Any]]:
        """
                Загружает вакансии из CSV файла.

                Returns:
                    List[Dict[str, Any]]: Список словарей с данными вакансий

                Notes:
                    Если файл не существует, возвращает пустой список
                    Все значения возвращаются как строки
                """
        if not os.path.exists(self._filename):
            return []

        with open(self._filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return list(reader)

    def save_vacancies(self, data: List[Dict[str, Any]]) -> None:
        """
                Сохраняет вакансии в CSV файл с заголовками.

                Args:
                    data: Список словарей с данными вакансий для сохранения

                Notes:
                    Если data пуст, файл не создается
                    Использует первую вакансию для определения заголовков
                """
        if not data:
            return

        fieldnames = data[0].keys()
        with open(self._filename, "w", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)


class TxtSaver(FileSaver):
    """
        Класс для сохранения и загрузки вакансий в текстовом формате (JSONL).

        Inherits:
            FileSaver: Базовый класс для работы с файлами

        Notes:
            Каждая вакансия сохраняется в отдельной строке как JSON объект
        """

    def __init__(self, filename: str = "vacancies.txt") -> None:
        """
                Инициализирует TxtSaver с именем файла по умолчанию.

                Args:
                    filename: Имя текстового файла (по умолчанию: vacancies.txt)
                """
        super().__init__(filename)

    def load_vacancies(self) -> List[Dict[str, Any]]:
        """
                Загружает вакансии из текстового файла (JSONL формат).

                Returns:
                    List[Dict[str, Any]]: Список словарей с данными вакансий

                Notes:
                    Если файл не существует, возвращает пустой список
                    Пропускает пустые строки и невалидные JSON объекты
                """
        if not os.path.exists(self._filename):
            return []
        with open(self._filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
            return [json.loads(line.strip()) for line in lines if line.strip()]

    def save_vacancies(self, data: List[Dict[str, Any]]) -> None:
        """
                Сохраняет вакансии в текстовый файл в формате JSONL.

                Args:
                    data: Список словарей с данными вакансий для сохранения

                Notes:
                    Каждая вакансия сохраняется в отдельной строке как JSON объект
                    Обеспечивает корректную кодировку UTF-8
                """
        with open(self._filename, "w", encoding="utf-8") as file:
            for vacancy in data:
                file.write(json.dumps(vacancy, ensure_ascii=False) + "\n")
