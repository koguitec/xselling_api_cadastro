"""Module for the Transaction in memory repository"""
from typing import Dict, List

from src.domain.transaction import Transaction


class MemRepoTransaction:
    """Class for the Product in memory repository"""

    def __init__(self, data: List[Dict]) -> None:
        self.data = data

    def list_transaction(self, filters=None) -> List:
        result = [Transaction.from_dict(c) for c in self.data]

        if filters is None:
            return result

        if 'id__eq' in filters:
            result = [c for c in result if c.code == filters['id__eq']]

        if 'code__eq' in filters:
            result = [c for c in result if c.code == filters['code__eq']]

        if 'ativo__eq' in filters:
            result = [c for c in result if c.ativo is filters['ativo__eq']]

        return result

    def create_transaction(self, product: Transaction) -> None:
        self.data.append(product)

        return product
