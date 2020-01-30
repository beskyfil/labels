from abc import ABCMeta, abstractmethod

class Service(metaclass=ABCMeta):
    """Abstract class of service which will be suported by this label-syncing app,
    this is just to make sure you dont forget to implement any of these required methods
    """
    @abstractmethod
    def __init__(self, config, name, api_url):
        """
        :param config: Config object
        :param name: Name of the service, i.e. 'github'
        :param api_url: Base API url for the service
        """
        pass

    @abstractmethod
    def apply_new_config(self, hook=None):
        """
        This method is called whenever config repo changes, is it responsible to correctly update service's repos.

        :param hook: hook payload from which is extracted what type of change happened in config, create, delete or edited label
        """
        pass

    @abstractmethod
    def update_labels(self, owner, repo):
        """
        This method is used for initial updating of repos after app start, it compares existing labels against config labels,
        if there is conflict, label will be changed according to config

        :param owner: owner of the repo
        :param repo: repo name
        """
        pass

    @abstractmethod
    def communication(self, token):
        """
        Method used to set up http session with service's API

        :param token: Secrive token
        """
        pass

    @abstractmethod
    def handle_incoming_hook(self, hook):
        """
        Core method which handles change in one of service's repos, based on type of change in incoming hook, 
        it either creates label, if it was deleted against the rules, or edits back to default state if it was incorrectly edited

        :return: tuple (string, int) where string is verbose status code meaninng, int is status code of the API operation result
        """
        pass
