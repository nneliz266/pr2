"""
NuGet repository implementation - аналог C# Repository
"""
import urllib.request
import urllib.error
import json
import xml.etree.ElementTree as ET
from typing import List


class NuGetRepository:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')

    def get_package_dependencies(self, package_name: str) -> List[str]:
        """
        Получение зависимостей пакета из NuGet репозитория
        Аналог C# метода получения зависимостей
        """
        try:
            # Пробуем разные API endpoints как в C# версии
            dependencies = self._try_v3_api(package_name)
            if not dependencies:
                dependencies = self._try_v2_api(package_name)

            return dependencies

        except Exception as e:
            raise Exception(f"Failed to get dependencies for {package_name}: {e}")

    def _try_v3_api(self, package_name: str) -> List[str]:
        """Попытка использовать V3 API"""
        try:
            url = f"{self.base_url}/{package_name.lower()}/index.json"

            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode('utf-8'))

            dependencies = []
            # Обход структуры JSON как в C# версии
            for item in data.get('items', []):
                for subitem in item.get('items', []):
                    catalog_entry = subitem.get('catalogEntry', {})
                    for dep_group in catalog_entry.get('dependencyGroups', []):
                        for dep in dep_group.get('dependencies', []):
                            dep_id = dep.get('id', '')
                            if dep_id and dep_id != package_name:
                                dependencies.append(dep_id)

            return list(set(dependencies))

        except:
            return []

    def _try_v2_api(self, package_name: str) -> List[str]:
        """Попытка использовать V2 API"""
        try:
            url = f"{self.base_url}/Packages(Id='{package_name}')"

            with urllib.request.urlopen(url) as response:
                content = response.read().decode('utf-8')

            # Парсинг XML как в C# версии
            root = ET.fromstring(content)
            dependencies = []

            # Namespaces для XML
            ns = {
                'atom': 'http://www.w3.org/2005/Atom',
                'm': 'http://schemas.microsoft.com/ado/2007/08/dataservices/metadata',
                'd': 'http://schemas.microsoft.com/ado/2007/08/dataservices'
            }

            # Поиск элемента зависимостей
            properties = root.find('.//m:properties', ns)
            if properties is not None:
                deps_elem = properties.find('d:Dependencies', ns)
                if deps_elem is not None and deps_elem.text:
                    # Формат: "Package1:Version1|Package2:Version2"
                    for dep_entry in deps_elem.text.split('|'):
                        if ':' in dep_entry:
                            dep_name = dep_entry.split(':')[0].strip()
                            if dep_name and dep_name != package_name:
                                dependencies.append(dep_name)

            return dependencies

        except:
            return []