from service import Service
import requests
from conf import Config
import helpers

class Github(Service):
    """
    Class which communicate with github API, handles webhooks about changes in repos, manages github repositories
    """
    def __init__(self, config, name, api_url):
        self.config = config
        self.name = name
        self.communication(self.config.get_github_token())
        self.api_url = api_url
        self.repos = self.config.get_repos_for_service(self.name)

        self.config.bind_to(self.apply_new_config)
        self.apply_new_config()

    def create_label(self, owner, repo, label):
        r = self.session.post(f'{self.api_url}/{owner}/{repo}/labels', json=label)
        if r.status_code != 201:
            raise helpers.HTTPError(f'Error {r.status_code} in POST request: {r.json()["message"]}')

    def edit_label(self, owner, repo, label, label_name):
        r = self.session.patch(f'{self.api_url}/{owner}/{repo}/labels/{label_name}', json=label)
        if r.status_code != 200:
            raise helpers.HTTPError(f'Error {r.status_code} in PATCH request: {r.json()["message"]}')

    def delete_label(self, owner, repo, label_name):
        r = self.session.delete(f'{self.api_url}/{owner}/{repo}/labels/{label_name}')
        if r.status_code != 204:
            raise helpers.HTTPError(f'Error {r.status_code} in DELETE request: {r.json()["message"]}')

    def apply_new_config(self, hook=None):
        if hook:
            payload = hook.get_json()
            if payload['action'] == 'created':
                for reposlug in self.repos:
                    self.create_label(reposlug["owner"], reposlug["repo"], payload['label'])
            if payload['action'] == 'edited':
                old_name = payload['label']['name']
                if 'name' in payload['changes']:
                    old_name = payload['changes']['name']['from']
                for reposlug in self.repos:
                    self.edit_label(reposlug["owner"], reposlug["repo"], payload['label'], old_name)
            if payload['action'] == 'deleted':
                for reposlug in self.repos:
                    self.delete_label(reposlug["owner"], reposlug["repo"], payload['label']['name'])
        else:
            for reposlug in self.repos:
                self.update_labels(reposlug["owner"], reposlug["repo"])

    def update_labels(self, owner, repo):
        r = self.session.get(f'{self.api_url}/{owner}/{repo}/labels')
        if r.status_code != 200:
            raise helpers.HTTPError(f'error {r.status_code} in GET request: {r.json()["message"]}')
        existing_labels = r.json()
        existing_names = [label['name'] for label in existing_labels]

        for label_name, label in self.config.config_labels.items():
            if label_name in existing_names:
                self.edit_label(owner, repo, label, label['name'])
            else:
                self.create_label(owner, repo, label)

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
                if n in self.config.config_labels.keys():
                    label = self.config.config_labels[n]
                    self.create_label(owner, repo, label)
            elif payload['action'] == 'edited':
                old_name = n
                if 'name' in payload['changes']:
                    old_name = payload['changes']['name']['from']
                if old_name in self.config.config_labels.keys():
                    label = self.config.config_labels[old_name]
                    self.edit_label(owner, repo, label, n)
            elif payload['action'] == 'created':
                return 'created hook action ignored', 200
        return 'hook was processed', 200

    def communication(self, token):
        self.session = requests.Session()
        self.session.headers = {'User-Agent': 'label sync bot', 'Authorization' : f'token {token}'}