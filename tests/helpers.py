import os
from labelsync.conf import Config
import requests

ABS_PATH = os.path.abspath(os.path.dirname(__file__))
FIXTURES_PATH = os.path.join(ABS_PATH, 'fixtures/')

class fl:
    def __init__(self, name):
        self.name = name

def create_cfg_env(fixture_name):
    cfg_name = fl(FIXTURES_PATH + fixture_name)
    c = Config(cfg_name)
    return c

def get_labels(owner, repo):
    r = requests.get(f'https://api.github.com/repos/{owner}/{repo}/labels')
    if r.status_code != 200:
        raise HTTPError(f'error {r.status_code} in GET request: {r.json()}')
    existing_names = [label['name'] for label in r.json()]
    return existing_names
