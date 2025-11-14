"""
Models for package data - аналог C# Models
"""
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class PackageInfo:
    """Информация о пакете"""
    name: str
    version: Optional[str] = None
    dependencies: List[str] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []

@dataclass
class DependencyGraph:
    """Граф зависимостей"""
    packages: dict  # name -> PackageInfo
    edges: list     # (from, to) tuples

    def __init__(self):
        self.packages = {}
        self.edges = []