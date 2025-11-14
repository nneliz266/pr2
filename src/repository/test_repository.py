"""
Test repository implementation
"""
import json
import os
from typing import List, Dict


class TestRepository:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._data = self._load_test_data()

    def _load_test_data(self) -> Dict[str, List[str]]:
        """Загрузка тестовых данных"""
        if not os.path.exists(self.file_path):
            # Создаем пример данных если файла нет
            default_data = {
                "A": ["B", "C"],
                "B": ["C", "D"],
                "C": ["E"],
                "D": ["F"],
                "E": ["B"],  # Цикл
                "F": []
            }
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            with open(self.file_path, 'w') as f:
                json.dump(default_data, f, indent=2)
            return default_data

        with open(self.file_path, 'r') as f:
            return json.load(f)

    def get_package_dependencies(self, package_name: str) -> List[str]:
        """Получение зависимостей из тестового репозитория"""
        if package_name not in self._data:
            raise ValueError(f"Package '{package_name}' not found in test repository")
        return self._data[package_name]