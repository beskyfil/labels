from service import Service
import requests
from conf import Config
import hashlib
import hmac

class Github(Service):
    def __init__(self, config):
        self.config = config
        self.login, self.token = self.config.get_github_login()
        self.api_url = 'https://api.github.com/repos'
        self.communication()
        _, owner, repo = self.config.get_repo_with_labels().split('/')
        self.req_labels = self.get_labels(owner, repo)
        self.req_labels_names = [label['name'] for label in self.req_labels]
        self.req_labels_map = {}
        for label in self.req_labels:
            self.req_labels_map[label['name']] = label

    def get_labels(self, owner, repo):
        r = requests.get(f'{self.api_url}/{owner}/{repo}/labels')
        labels = r.json()
        return labels

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
            print(r.status_code)
            print(r.json())

    def handle_incoming_hook(self, payload):
        ret, code = self.check_hook(payload)
        if ret != 200:
            return ret, code
        if payload.headers['X-GitHub-Event'] == 'label':
            body = payload.json()
            if body['label']['name'] in self.req_labels_names:
                owner = body['repository']['owner']['login']
                repo = body['repository']['name']
                if body['action'] == 'deleted':
                    self.session.post(f'{self.api_url}/{owner}/{repo}/labels', json=body['label'])
                elif body['action'] == 'edited':
                    n = body['label']['name']
                    if not 'name' in body['changes']:
                        old_name = n
                    else:
                        old_name = body['changes']['from']
                    label = self.req_labels_map[old_name]
                    self.session.patch(f'{self.api_url}/{owner}/{repo}/labels/{n}', json=label)
                elif body['action'] == 'created':
                    return 'created hook action ignored', 200
        return 'hook was processed', 200

    def check_hook(self, payload):
        if not "X-Hub-Signature" in payload.headers:
            return "OK, but unsafe", 200
        request_signature = payload.headers["X-Hub-Signature"].split('=')
        secret = self.config.get_secret()
        secret = secret.encode("utf-8")
        digest = hmac.new(secret, payload.data, hashlib.sha1).hexdigest()
        if len(request_signature) < 2 or request_signature[0] != 'sha1' or not hmac.compare_digest(request_signature[1], digest):
            return 'Invalid signature!', 400
        return 'OK, valid signature', 200

    # def create_webhook(self, owner, repo):
    #     self.session.post(f'{self.api_url}/{owner}/{repo}/hooks', json=hook_config)

    def communication(self):
        self.session = requests.Session()
        self.session.headers = {'User-Agent': 'Github label sync bot', 'Authorization' : f'token {self.token}'}

        #check if i can do somethign with this repo
        # r = self.session.get(f'https://api.github.com/repos/{self.reposlug}/issues')
        # if r.status_code != 200:
        #     raise RuntimeError('invalid repo')
