from abc import ABC, abstractmethod

class BaseScheduler(ABC):

    @abstractmethod
    def register(self, scheduler):
        pass
