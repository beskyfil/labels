from service import Service
import requests
from conf import Config
import helpers

class Github(Service):
    def __init__(self, config):
        self.config = config
        self.login, self.token = self.config.get_github_login()
        self.communication()
        self.api_url = 'https://api.github.com/repos'
        self.repos = [{'owner':r.split('/')[1], 'repo':r.split('/')[2]} for r in self.config.get_repos_to_synch() if r.split('/')[0] == 'github']

        self.config.bind_to(self.apply_new_config)
        self.apply_new_config(None, self.config.config_labels)

    def apply_new_config(self, hook, config_labels):
        self.req_labels = config_labels
        if hook:
            payload = hook.get_json()
            label_name = payload['label']['name']
            if payload['action'] == 'created':
                for reposlug in self.repos:
                    self.session.post(f'{self.api_url}/{reposlug["owner"]}/{reposlug["repo"]}/labels', json=payload['label'])
            if payload['action'] == 'edited':
                if 'name' in payload['changes']:
                    label_name = payload['changes']['name']['from']
                for reposlug in self.repos:
                    self.session.patch(f'{self.api_url}/{reposlug["owner"]}/{reposlug["repo"]}/labels/{label_name}', json=payload['label'])
            if payload['action'] == 'deleted':
                for reposlug in self.repos:
                    self.session.delete(f'{self.api_url}/{reposlug["owner"]}/{reposlug["repo"]}/labels/{label_name}')
        else:
            for reposlug in self.repos:
                self.update_labels(reposlug["owner"], reposlug["repo"])

    def update_labels(self, owner, repo):
        r = self.session.get(f'{self.api_url}/{owner}/{repo}/labels')
        existing_labels = r.json()
        existing_names = [label['name'] for label in existing_labels]

        for label_name, label in self.req_labels.items():
            if label_name in existing_names:
                r = self.session.patch(f'{self.api_url}/{owner}/{repo}/labels/{label_name}', json=label)
            else:
                r = self.session.post(f'{self.api_url}/{owner}/{repo}/labels', json=label)
            # print(r.status_code)
            # print(r.json())

    def handle_incoming_hook(self, hook):
        ret, code = helpers.check_github_hook(hook, self.config.get_secret())
        if code != 200:
            return ret, code
        if hook.headers['X-GitHub-Event'] == 'label':
            payload = hook.get_json()
            owner = payload['repository']['owner']['login']
            repo = payload['repository']['name']
            n = payload['label']['name']
            if payload['action'] == 'deleted':
                if n in self.req_labels.keys():
                    label = self.req_labels[n]
                    self.session.post(f'{self.api_url}/{owner}/{repo}/labels', json=label)
            elif payload['action'] == 'edited':
                old_name = n
                if 'name' in payload['changes']:
                    old_name = payload['changes']['name']['from']
                if old_name in self.req_labels.keys():
                    label = self.req_labels[old_name]
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
