"""Module for the base class for domain models"""
# pylint: disable=c0115
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(kw_only=True)
class BaseDomainModel:
    """Base class for the domain models.
    They all inherit the attributes from this class.
    """

    id: Optional[int] = None
    code: Optional[uuid.UUID] = None
    dt_inclusao: datetime = None
    dt_alteracao: datetime = None
    ativo: bool = True
