from service import Service
import requests
from conf import Config

class Github(Service):
    def __init__(self, config):
        self.config = config
        self.login, self.token = self.config.get_github_login()
        self.api_url = 'https://api.github.com/repos'
        self.communication()
        self.req_labels = self.config.config_labels
        self.req_labels_names = [label['name'] for label in self.req_labels]
        self.req_labels_map = {}
        for label in self.req_labels:
            self.req_labels_map[label['name']] = label

    def update_labels(self, owner, repo):
        r = self.session.get(f'{self.api_url}/{owner}/{repo}/labels')
        existing_labels = r.json()
        existing_names = [label['name'] for label in existing_labels]

        for label in self.req_labels:
            n = label['name']
            if n in existing_names:
                r = self.session.patch(f'{self.api_url}/{owner}/{repo}/labels/{n}', json=label)
            else:
                r = self.session.post(f'{self.api_url}/{owner}/{repo}/labels', json=label)
            # print(r.status_code)
            # print(r.json())

    def handle_incoming_hook(self, hook):
        ret, code = self.config.check_hook(hook)
        if code != 200:
            return ret, code
        if hook.headers['X-GitHub-Event'] == 'label':
            payload = hook.get_json()
            # print(payload['action'])
            # print(payload['label']['name'])
            owner = payload['repository']['owner']['login']
            repo = payload['repository']['name']
            n = payload['label']['name']
            if payload['action'] == 'deleted':
                if n in self.req_labels_names:
                    label = self.req_labels_map[n]
                    self.session.post(f'{self.api_url}/{owner}/{repo}/labels', json=label)
            elif payload['action'] == 'edited':
                # print(payload['changes'])
                old_name = n
                if 'name' in payload['changes']:
                    old_name = payload['changes']['name']['from']
                if old_name in self.req_labels_names:
                    label = self.req_labels_map[old_name]
                    self.session.patch(f'{self.api_url}/{owner}/{repo}/labels/{n}', json=label)
            elif payload['action'] == 'created':
                return 'created hook action ignored', 200
        return 'hook was processed', 200

    def communication(self):
        self.session = requests.Session()
        self.session.headers = {'User-Agent': 'Github label sync bot', 'Authorization' : f'token {self.token}'}

        #check if i can do somethign with this repo
        # r = self.session.get(f'https://api.github.com/repos/{self.reposlug}/issues')
        # if r.status_code != 200:
        #     raise RuntimeError('invalid repo')
