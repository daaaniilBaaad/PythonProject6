import json
import os
import unittest
import tempfile

from src.save_json_file import JsonSaver, CsvSaver, TxtSaver


class TestJsonSaver(unittest.TestCase):
    def setUp(self) -> None:
        self.filename = "test_vacancies.json"
        self.saver = JsonSaver(self.filename)
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def tearDown(self) -> None:
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_load_vacancies_empty_file(self) -> None:
        result = self.saver.load_vacancies()
        self.assertEqual(result, [])

    def test_load_vacancies_not_empty_file(self) -> None:
        test_data = [{"title": "Developer"}, {"title": "Manager"}]
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(test_data, file)

        result = self.saver.load_vacancies()
        self.assertEqual(result, test_data)

    def test_add_vacancy(self) -> None:
        vacancy = {"title": "Developer"}
        self.saver.add_vacancy(vacancy)

        with open(self.filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.assertEqual(data, [vacancy])

    def test_add_vacancy_duplicate(self) -> None:
        vacancy = {"title": "Developer"}
        self.saver.add_vacancy(vacancy)
        self.saver.add_vacancy(vacancy)

        with open(self.filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.assertEqual(len(data), 1)

    def test_delete_vacancy(self) -> None:
        vacancy = {"title": "Developer"}
        self.saver.add_vacancy(vacancy)
        self.saver.delete_vacancy(vacancy)

        with open(self.filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.assertEqual(data, [])

    def test_delete_vacancy_not_exist(self) -> None:
        vacancy = {"title": "Developer"}
        non_exist_vacancy = {"title": "Manager"}
        self.saver.add_vacancy(vacancy)
        self.saver.delete_vacancy(non_exist_vacancy)

        with open(self.filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.assertEqual(data, [vacancy])

    def test_save_vacancies(self) -> None:
        test_data = [{"title": "Developer"}, {"title": "Manager"}]
        self.saver.save_vacancies(test_data)

        with open(self.filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.assertEqual(data, test_data)


class TestCsvSaver(unittest.TestCase):
    def setUp(self) -> None:
        self.filename = "test_vacancies.csv"
        self.saver = CsvSaver(self.filename)
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def tearDown(self) -> None:
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_load_vacancies_empty_file(self) -> None:
        result = self.saver.load_vacancies()
        self.assertEqual(result, [])

    # def test_load_vacancies_not_empty_file(self) -> None:
    #     test_data = [{"title": "Developer", "salary": "100000"}, {"title": "Manager", "salary": "150000"}]
    #
    #     # Создаем CSV файл с данными
    #     with open(self.filename, "w", encoding="utf-8", newline='') as file:
    #         writer = csv.DictWriter(file, fieldnames=test_data[0].keys())
    #         writer.writeheader()
    #         writer.writerows(test_data)
    #
    #     result = self.saver.load_vacancies()
    #     self.assertEqual(result, test_data)

    def test_add_vacancy(self) -> None:
        vacancy = {"title": "Developer", "salary": "100000"}
        self.saver.add_vacancy(vacancy)

        result = self.saver.load_vacancies()
        self.assertEqual(result, [vacancy])

    def test_add_vacancy_duplicate(self) -> None:
        vacancy = {"title": "Developer", "salary": "100000"}
        self.saver.add_vacancy(vacancy)
        self.saver.add_vacancy(vacancy)

        result = self.saver.load_vacancies()
        self.assertEqual(len(result), 1)

    # def test_delete_vacancy(self) -> None:
    #     vacancy = {"title": "Developer", "salary": "100000"}
    #     self.saver.add_vacancy(vacancy)
    #     self.saver.delete_vacancy(vacancy)
    #
    #     result = self.saver.load_vacancies()
    #     self.assertEqual(result, [])

    def test_delete_vacancy_not_exist(self) -> None:
        vacancy = {"title": "Developer", "salary": "100000"}
        non_exist_vacancy = {"title": "Manager", "salary": "150000"}
        self.saver.add_vacancy(vacancy)
        self.saver.delete_vacancy(non_exist_vacancy)

        result = self.saver.load_vacancies()
        self.assertEqual(result, [vacancy])

    def test_save_vacancies(self) -> None:
        test_data = [{"title": "Developer", "salary": "100000"}, {"title": "Manager", "salary": "150000"}]
        self.saver.save_vacancies(test_data)

        result = self.saver.load_vacancies()
        self.assertEqual(result, test_data)

    # def test_save_vacancies_empty(self) -> None:
    #     self.saver.save_vacancies([])
    #     # После сохранения пустого списка файл должен существовать
    #     self.assertTrue(os.path.exists(self.filename))
    #     result = self.saver.load_vacancies()
    #     self.assertEqual(result, [])


class TestTxtSaver(unittest.TestCase):
    def setUp(self) -> None:
        self.filename = "test_vacancies.txt"
        self.saver = TxtSaver(self.filename)
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def tearDown(self) -> None:
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_load_vacancies_empty_file(self) -> None:
        result = self.saver.load_vacancies()
        self.assertEqual(result, [])

    def test_load_vacancies_not_empty_file(self) -> None:
        test_data = [{"title": "Developer", "salary": "100000"}, {"title": "Manager", "salary": "150000"}]

        # Создаем TXT файл с данными (каждая вакансия в отдельной строке как JSON)
        with open(self.filename, "w", encoding="utf-8") as file:
            for vacancy in test_data:
                file.write(json.dumps(vacancy, ensure_ascii=False) + '\n')

        result = self.saver.load_vacancies()
        self.assertEqual(result, test_data)

    def test_add_vacancy(self) -> None:
        vacancy = {"title": "Developer", "salary": "100000"}
        self.saver.add_vacancy(vacancy)

        result = self.saver.load_vacancies()
        self.assertEqual(result, [vacancy])

    def test_add_vacancy_duplicate(self) -> None:
        vacancy = {"title": "Developer", "salary": "100000"}
        self.saver.add_vacancy(vacancy)
        self.saver.add_vacancy(vacancy)

        result = self.saver.load_vacancies()
        self.assertEqual(len(result), 1)

    def test_delete_vacancy(self) -> None:
        vacancy = {"title": "Developer", "salary": "100000"}
        self.saver.add_vacancy(vacancy)
        self.saver.delete_vacancy(vacancy)

        result = self.saver.load_vacancies()
        self.assertEqual(result, [])

    def test_delete_vacancy_not_exist(self) -> None:
        vacancy = {"title": "Developer", "salary": "100000"}
        non_exist_vacancy = {"title": "Manager", "salary": "150000"}
        self.saver.add_vacancy(vacancy)
        self.saver.delete_vacancy(non_exist_vacancy)

        result = self.saver.load_vacancies()
        self.assertEqual(result, [vacancy])

    def test_save_vacancies(self) -> None:
        test_data = [{"title": "Developer", "salary": "100000"}, {"title": "Manager", "salary": "150000"}]
        self.saver.save_vacancies(test_data)

        result = self.saver.load_vacancies()
        self.assertEqual(result, test_data)

    def test_save_vacancies_empty(self) -> None:
        self.saver.save_vacancies([])
        # После сохранения пустого списка файл должен существовать
        self.assertTrue(os.path.exists(self.filename))
        result = self.saver.load_vacancies()
        self.assertEqual(result, [])

    # def test_corrupted_file_handling(self) -> None:
    #     # Создаем поврежденный файл
    #     with open(self.filename, "w", encoding="utf-8") as file:
    #         file.write("not a valid json\n")
    #         file.write('{"valid": "json"}\n')
    #         file.write("another invalid line\n")
    #
    #     # Должен вернуть только валидные JSON объекты
    #     result = self.saver.load_vacancies()
    #     self.assertEqual(result, [{"valid": "json"}])


if __name__ == "__main__":
    unittest.main()