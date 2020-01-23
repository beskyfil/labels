from abc import ABCMeta, abstractmethod

class Service(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, config):
        pass

    @abstractmethod
    def update_labels(self, repo):
        pass

    @abstractmethod
    def communication(self):
        pass

    @abstractmethod
    def handle_incoming_hook(self):
        pass

    # @abstractmethod
    # def create_webhook(self):
    #     pass