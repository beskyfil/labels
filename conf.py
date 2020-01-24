import configparser
import os
import requests
import hashlib
import hmac

class Config:
    def __init__(self, _cfg_file_name):
        self._cfg_file_name = _cfg_file_name
        self.config = configparser.ConfigParser()
        self.config.read(_cfg_file_name)
        self.check_config()
        self.auth_conf = os.environ['AUTH_CONFIG']
        self.config_labels = self.get_config_labels()

    def handle_incoming_hook(self, request):
        pass

    def check_hook(self, hook):
        if not "X-Hub-Signature" in hook.headers:
            return "OK, but unsafe", 200
        request_signature = hook.headers["X-Hub-Signature"].split('=')
        secret = self.get_secret()
        secret = secret.encode("utf-8")
        digest = hmac.new(secret, hook.data, hashlib.sha1).hexdigest()
        if len(request_signature) < 2 or request_signature[0] != 'sha1' or not hmac.compare_digest(request_signature[1], digest):
            return 'Invalid signature!', 400
        return 'OK, valid signature', 200

    def get_config_labels(self):
        _, owner, repo = self.get_repo_with_labels().split('/')
        r = requests.get(f'https://api.github.com/repos/{owner}/{repo}/labels')
        labels = r.json()
        return labels
    
    def check_config(self):
        if not all(s in ['labels_loc', 'repos', 'services', 'secret'] for s in self.config.sections()):
            raise RuntimeError('config error')

        if not os.getenv('AUTH_CONFIG'):
            raise RuntimeError('no AUTH_CONFIG environment variable set')

    def get_repo_with_labels(self):
        return self.config['labels_loc']['l']

    def get_repos_to_synch(self):
        return [self.config['repos'][r] for r in self.config['repos']]

    def get_secret(self):
        return self.config['secret']['secret']

    # username:token
    def get_github_login(self):
        return self.auth_conf.split(':')[0], self.auth_conf.split(':')[1]
