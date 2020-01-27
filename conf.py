import configparser
import os
import requests
import hashlib
import hmac
import helpers
from pathlib import Path

class Config():
    def __init__(self, _cfg_file_name):
        self._cfg_file_name = _cfg_file_name
        self.config = configparser.ConfigParser()
        self.config.read(Path(_cfg_file_name))
        self.check_config()
        self.auth_conf = os.environ['AUTH_CONFIG']
        self.gitlab_conf = os.environ['GITLAB_CONFIG']
        self.secret = self.get_secret()
        self.config_labels = self.get_config_labels()
        self._observers = []

    def bind_to(self, callback):
        print('bound')
        self._observers.append(callback)

    def get_repos_for_service(self, service_name):
        return [{'owner':r.split('/')[1], 'repo':r.split('/')[2]} for r in self.get_repos_to_synch() if r.split('/')[0] == service_name]

    def handle_incoming_hook(self, hook):
        ret, code = helpers.check_github_hook(hook, self.secret)
        if code != 200:
            return ret, code

        self.config_labels = self.get_config_labels()
        for callback in self._observers:
            print('announcing change')
            callback(hook, self.config_labels)
        return 'ok', 200

    def get_config_labels(self):
        _, owner, repo = self.get_repo_with_labels().split('/')
        r = requests.get(f'https://api.github.com/repos/{owner}/{repo}/labels').json()
        labels = {}
        for label in r:
            labels[label['name']] = {'name':label['name'], 'color':label['color'], 'description':label['description']}
        return labels
    
    def check_config(self):
        if not all(s in ['labels_loc', 'repos', 'services', 'secret'] for s in self.config.sections()):
            raise RuntimeError('config error')

        if not os.getenv('AUTH_CONFIG'):
            raise RuntimeError('no AUTH_CONFIG environment variable set')

        if not os.getenv('GITLAB_CONFIG'):
            raise RuntimeError('no GITLAB_CONFIG environment variable set')

    def get_repo_with_labels(self):
        return self.config['labels_loc']['l']

    def get_repos_to_synch(self):
        return [self.config['repos'][r] for r in self.config['repos']]

    def get_secret(self):
        return self.config['secret']['secret']

    # username:token
    def get_github_login(self):
        return self.auth_conf.split(':')[0], self.auth_conf.split(':')[1]

    def get_gitlab_login(self):
        return self.gitlab_conf
