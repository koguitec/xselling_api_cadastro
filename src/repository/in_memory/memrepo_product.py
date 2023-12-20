"""Module for the Product in memory repository"""
from typing import Dict, List

from src.domain.product import Product


class MemRepoProduct:
    """Class for the Product in memory repository"""

    def __init__(self, data: List[Dict]) -> None:
        self.data = data

    def list_product(self, filters=None) -> List:
        result = [Product.from_dict(c) for c in self.data]

        if filters is None:
            return result

        if 'id__eq' in filters:
            result = [c for c in result if c.code == filters['id__eq']]

        if 'code__eq' in filters:
            result = [c for c in result if c.code == filters['code__eq']]

        if 'ativo__eq' in filters:
            result = [c for c in result if c.ativo is filters['ativo__eq']]

        return result

    def create_product(self, product: Product) -> None:
        self.data.append(product)

        return product
