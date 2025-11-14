"""
Command line parser - аналог C# CommandLineParser
"""
import argparse


class CommandLineParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='NuGet Package Dependency Visualizer',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        self._setup_arguments()

    def _setup_arguments(self):
        """Настройка аргументов командной строки"""
        # Основные параметры
        self.parser.add_argument(
            '--package', '-p',
            required=True,
            help='Name of the package to analyze'
        )

        self.parser.add_argument(
            '--source', '-s',
            required=True,
            help='Repository URL or path to test repository file'
        )

        self.parser.add_argument(
            '--test-mode',
            action='store_true',
            help='Enable test repository mode'
        )

        self.parser.add_argument(
            '--reverse', '-r',
            action='store_true',
            help='Show reverse dependencies for specified package'
        )

    def parse_args(self):
        """Парсинг аргументов с валидацией"""
        args = self.parser.parse_args()

        # Этап 1: Вывод параметров конфигурации
        self._print_configuration(args)

        # Валидация параметров
        self._validate_args(args)

        return args

    def _print_configuration(self, args):
        """Вывод параметров в формате ключ-значение"""
        print("=== CONFIGURATION PARAMETERS ===")
        print(f"Package: {args.package}")
        print(f"Source: {args.source}")
        print(f"Test Mode: {args.test_mode}")
        print(f"Reverse Dependencies: {args.reverse}")
        print("================================")

    def _validate_args(self, args):
        """Валидация аргументов командной строки"""
        if args.test_mode:
            # Для тестового режима проверяем существование файла
            import os
            if not os.path.exists(args.source):
                raise ValueError(f"Test repository file not found: {args.source}")
        else:
            # Для реального режима проверяем URL
            if not args.source.startswith(('http://', 'https://')):
                raise ValueError(f"Invalid repository URL: {args.source}")