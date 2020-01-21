from abc import ABCMeta, abstractmethod

class Service(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def abc(self):
        pass