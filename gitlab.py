from service import Service
import requests
from conf import Config
import helpers

class Gitlab(Service):
    def __init__(self, config, name, api_url):
        self.config = config
        self.name = name
        self.communication(self.config.get_gitlab_token())
        self.api_url = api_url
        self.repos = self.config.get_repos_for_service(self.name)

        self.config.bind_to(self.apply_new_config)
        self.apply_new_config()

    def create_label(self, owner, repo, label):
        r = self.session.post(f'{self.api_url}/{owner}%2F{repo}/labels', json=label)
        if r.status_code != 201:
            raise helpers.HTTPError(f'Error {r.status_code} in POST request: {r.json()}')

    def edit_label(self, owner, repo, label, label_name):
        r = self.session.put(f'{self.api_url}/{owner}%2F{repo}/labels/{label_name}', json=label)
        if r.status_code != 200:
            raise helpers.HTTPError(f'Error {r.status_code} in PATCH request: {r.json()}')

    def delete_label(self, owner, repo, label_name):
        r = self.session.delete(f'{self.api_url}/{owner}%2F{repo}/labels/{label_name}')
        if r.status_code != 204:
            raise helpers.HTTPError(f'Error {r.status_code} in DELETE request: {r.json()}')

    def apply_new_config(self, hook=None):
        if hook:
            payload = hook.get_json()

            label_name = payload['label']['name']
            label = {'name':label_name, 'new_name':label_name}
            label['color'] = f"#{payload['label']['color']}"
            if 'description' in payload['label']:
                label['description'] = payload['label']['description']

            if payload['action'] == 'created':
                for reposlug in self.repos:
                    self.create_label(reposlug["owner"], reposlug["repo"], label)
            if payload['action'] == 'edited':
                if 'name' in payload['changes']:
                    label_name = payload['changes']['name']['from']
                for reposlug in self.repos:
                    self.edit_label(reposlug["owner"], reposlug["repo"], label, label_name)
            if payload['action'] == 'deleted':
                for reposlug in self.repos:
                    self.delete_label(reposlug["owner"], reposlug["repo"], label_name)
        else:
            for reposlug in self.repos:
                self.update_labels(reposlug["owner"], reposlug["repo"])

    def update_labels(self, owner, repo):
        r = self.session.get(f'{self.api_url}/{owner}%2F{repo}/labels')
        if r.status_code != 200:
            raise helpers.HTTPError(f'error {r.status_code} in GET request: {r.json()["message"]}')
        existing_labels = r.json()
        existing_names = [label['name'] for label in existing_labels]

        for label_name, label in self.config.config_labels.items():
            label_to_send = helpers.build_label(label)
            if label_name in existing_names:
                r = self.session.put(f'{self.api_url}/{owner}%2F{repo}/labels/{label_name}', json=label_to_send)
            else:
                r = self.session.post(f'{self.api_url}/{owner}%2F{repo}/labels', json=label_to_send)

    def handle_incoming_hook(self, hook):
        """Gitlab doesnt support label webhooking"""
        pass

    def communication(self, token):
        self.session = requests.Session()
        self.session.headers = {'User-Agent': 'label sync bot', 'Private-Token' : f'{token}'}
