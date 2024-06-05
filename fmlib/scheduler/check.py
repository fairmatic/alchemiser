from abc import ABC, abstractmethod
from enum import Enum


class IntervalType(Enum):
    SECONDS = "seconds"
    MINUTES = "minutes"
    HOURS = "hours"
    DAYS = "days"


class BaseTask(ABC):
    @property
    @abstractmethod
    def repeat_interval(self) -> int:
        pass

    @property
    @abstractmethod
    def interval_type(self) -> IntervalType:
        pass

    @classmethod
    def run_task(cls) -> None:
        cls.run()

    @classmethod
    @abstractmethod
    def run(cls):
        pass
