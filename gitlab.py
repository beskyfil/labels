from service import Service
import requests
from conf import Config
import helpers

class Gitlab(Service):
    def __init__(self, config):
        self.config = config
        self.token = self.config.get_gitlab_login()
        self.communication()
        self.api_url = 'https://gitlab.fit.cvut.cz/api/v4'
        self.repos = self.config.get_repos_for_service('gitlab')

        self.config.bind_to(self.apply_new_config)
        self.apply_new_config(None, self.config.config_labels)

    def apply_new_config(self, hook, config_labels):
        pass

    def update_labels(self, owner, repo):
        pass

    def handle_incoming_hook(self, hook):
        pass

    def communication(self):
        self.session = requests.Session()
        self.session.headers = {'User-Agent': 'label sync bot', 'Private-Token' : f'{self.token}'}