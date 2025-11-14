#!/usr/bin/env python3
"""
NuGet Dependency Visualizer - Вариант 13
"""

import sys
import os

# Добавляем текущую папку в Python path
sys.path.append(os.path.dirname(__file__))

# Импорты
from command_line.parser import CommandLineParser
from repository.nuget_repository import NuGetRepository
from repository.test_repository import TestRepository
from dependency_graph.builder import DependencyGraphBuilder
from visualization.plantuml_visualizer import PlantUMLVisualizer


def main():
    try:
        # Этап 1: Парсинг командной строки
        parser = CommandLineParser()
        args = parser.parse_args()

        # Выбор репозитория
        if args.test_mode:
            repository = TestRepository(args.source)
        else:
            repository = NuGetRepository(args.source)

        # Этап 2 и 3: Построение графа зависимостей
        graph_builder = DependencyGraphBuilder(repository)
        dependency_graph = graph_builder.build_graph(args.package)

        # Этап 4: Обратные зависимости или Этап 5: Визуализация
        if args.reverse:
            reverse_deps = graph_builder.find_reverse_dependencies(args.package)
            for dep in reverse_deps:
                print(f"  - {dep}")
        else:
            visualizer = PlantUMLVisualizer()
            plantuml_code = visualizer.generate(dependency_graph, args.package)
            print(plantuml_code)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()