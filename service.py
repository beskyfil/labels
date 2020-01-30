from abc import ABCMeta, abstractmethod

class Service(metaclass=ABCMeta):
    """Abstract class of service which will be suported by this label-syncing app,
    this is just to make sure you dont forget to implement any of these required methods
    """
    @abstractmethod
    def __init__(self, config, name, api_url):
        pass

    @abstractmethod
    def apply_new_config(self, hook):
        pass

    @abstractmethod
    def update_labels(self, owner, repo):
        pass

    @abstractmethod
    def communication(self, hook):
        pass

    @abstractmethod
    def handle_incoming_hook(self, token):
        pass
