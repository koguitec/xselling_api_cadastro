"""Module for the Transaction entity"""
import dataclasses
from datetime import datetime
from typing import Dict

from src.domain.base import BaseDomainModel


@dataclasses.dataclass()
class Transaction(BaseDomainModel):
    """Transaction entity"""

    client_id: int
    dt_transacao: datetime

    @classmethod
    def from_dict(cls, d: Dict):
        """Initialize an object from a dictionary

        Args:
            d (Dict): dictionary containing all class attributes

        Returns:
            Model: Instance of class object
        """
        return cls(**d)

    def to_dict(self):
        """Returns a dictinary from a class object

        Returns:
            Dict: dictionary containg all class attribute data
        """
        return dataclasses.asdict(self)
