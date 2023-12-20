"""Module for the Category entity"""
import dataclasses
from typing import Dict, List

from src.domain.base import BaseDomainModel


@dataclasses.dataclass()
class Category(BaseDomainModel):
    """Category entity"""

    descricao: str
    client_id: List[int]

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
