from abc import ABCMeta, abstractmethod

class Service(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def update_labels(self, repo):
        pass

    @abstractmethod
    def communication(self):
        pass