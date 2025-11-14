"""
Dependency graph builder - аналог C# DependencyGraph
"""
from collections import deque
from typing import List, Dict, Set, Tuple


class DependencyGraphBuilder:
    def __init__(self, repository):
        self.repository = repository
        self.cycles = set()

    def build_graph(self, root_package: str) -> Dict[str, List[str]]:
        """
        Построение графа зависимостей с помощью BFS
        Аналог C# реализации обхода графа
        """
        graph = {}
        visited = set()
        queue = deque([root_package])

        print(f"\nBuilding dependency graph for: {root_package}")

        while queue:
            current = queue.popleft()

            if current in visited:
                continue

            visited.add(current)

            try:
                # Получаем зависимости текущего пакета
                dependencies = self.repository.get_package_dependencies(current)
                graph[current] = dependencies

                # Этап 2: Вывод прямых зависимостей для корневого пакета
                if current == root_package:
                    print(f"Direct dependencies for {root_package}:")
                    for dep in dependencies:
                        print(f"  - {dep}")

                # Добавляем зависимости в очередь
                for dep in dependencies:
                    if dep not in visited:
                        # Проверка циклов
                        if self._is_cycle(graph, current, dep):
                            self.cycles.add((current, dep))
                            print(f"Cycle detected: {current} -> {dep}")
                        queue.append(dep)

            except Exception as e:
                print(f"Warning: Could not process {current}: {e}")
                graph[current] = []

        self._report_cycles()
        return graph

    def _is_cycle(self, graph: Dict[str, List[str]], from_pkg: str, to_pkg: str) -> bool:
        """Проверка наличия цикла"""
        if to_pkg in graph:
            return from_pkg in graph[to_pkg]
        return False

    def _report_cycles(self):
        """Отчет о найденных циклах"""
        if self.cycles:
            print(f"\nFound {len(self.cycles)} cyclic dependencies:")
            for cycle in self.cycles:
                print(f"  - {cycle[0]} <-> {cycle[1]}")

    def find_reverse_dependencies(self, target_package: str) -> List[str]:
        """Поиск обратных зависимостей"""
        # Для этого нужно сначала построить полный граф
        # В реальной реализации здесь будет логика поиска обратных зависимостей
        return [f"ReverseDep_{i}" for i in range(3)]  # Заглушка