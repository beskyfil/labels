from abc import ABCMeta, abstractmethod

class Service(metaclass=ABCMeta):
    """Abstract class of service this label-syncing app supports,
    this is just to make sure you dont forget to implement any of required methods"""
    @abstractmethod
    def __init__(self, config):
        pass

    @abstractmethod
    def update_labels(self):
        pass

    @abstractmethod
    def communication(self):
        pass

    @abstractmethod
    def handle_incoming_hook(self):
        pass

    @abstractmethod
    def apply_new_config(self):
        pass

    # @abstractmethod
    # def create_webhook(self):
    #     pass