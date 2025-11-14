"""
PlantUML visualizer - аналог C# Visualization
"""
from typing import Dict, List


class PlantUMLVisualizer:
    def generate(self, graph: Dict[str, List[str]], root_package: str) -> str:
        """
        Генерация PlantUML кода для визуализации графа
        Аналог C# визуализатора
        """
        lines = [
            "@startuml",
            "skinparam monochrome true",
            "skinparam shadowing false",
            "skinparam nodesep 10",
            "skinparam ranksep 30",
            ""
        ]

        # Добавляем корневой узел
        root_id = self._normalize_name(root_package)
        lines.append(f'rectangle "{root_package}" as {root_id} #lightblue')
        lines.append("")

        # Добавляем все узлы и связи
        added_nodes = {root_package: root_id}

        for package, dependencies in graph.items():
            pkg_id = self._normalize_name(package)

            if package not in added_nodes:
                lines.append(f'rectangle "{package}" as {pkg_id}')
                added_nodes[package] = pkg_id

            for dep in dependencies:
                dep_id = self._normalize_name(dep)
                if dep not in added_nodes:
                    lines.append(f'rectangle "{dep}" as {dep_id}')
                    added_nodes[dep] = dep_id

                lines.append(f'{pkg_id} --> {dep_id}')

        lines.append("@enduml")
        return "\n".join(lines)

    def _normalize_name(self, name: str) -> str:
        """Нормализация имени для PlantUML"""
        return name.replace('.', '_').replace('-', '_').replace(' ', '')