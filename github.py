from service import Service
import requests
from conf import Config

class Github(Service):
    def __init__(self, config):
        self.config = config
        self.login, self.token = self.config.get_github_login()
        self.api_url = 'https://api.github.com/repos'
        self.communication()

    def update_labels(self, owner, repo, req_labels):
        r = self.session.get(f'{self.api_url}/{owner}/{repo}/labels')
        existing_labels = r.json()
        existing_names = [label['name'] for label in existing_labels]

        for label in req_labels:
            n = label['name']
            if n in existing_names:
                r = self.session.patch(f'{self.api_url}/{owner}/{repo}/labels/{n}', json=label)
            else:
                r = self.session.post(f'{self.api_url}/{owner}/{repo}/labels', json=label)
            print(r.status_code)
            print(r.json())

    # def create_webhook(self, owner, repo):
    #     self.session.post(f'{self.api_url}/{owner}/{repo}/hooks', json=hook_config)

    def communication(self):
        self.session = requests.Session()
        self.session.headers = {'User-Agent': 'Github label sync bot', 'Authorization' : f'token {self.token}'}

        #check if i can do somethign with this repo
        # r = self.session.get(f'https://api.github.com/repos/{self.reposlug}/issues')
        # if r.status_code != 200:
        #     raise RuntimeError('invalid repo')
