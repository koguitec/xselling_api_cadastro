from abc import ABC, abstractmethod


class AlgorithmStrategyInterface(ABC):
    @abstractmethod
    def execute(self):
        pass
