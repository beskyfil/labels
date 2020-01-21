from service import Service
import requests
from conf import Config

class Github(Service):
    def __init__(self, config):
        self.config = config
        self.login, self.token = self.config.get_github_login()
        self.api_url = 'https://api.github.com/repos'
        self.communication()

    def update_labels(self):
        pass

    def communication(self):
        self.session = requests.Session()
        self.session.headers = {'User-Agent': 'Github label sync bot', 'Authorization' : f'token {self.token}'}

        #check if i can do somethign with this repo
        # r = self.session.get(f'https://api.github.com/repos/{self.reposlug}/issues')
        # if r.status_code != 200:
        #     raise RuntimeError('invalid repo')
