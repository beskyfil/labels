from flask import Flask, escape, request
from conf import Config
from github import Github
import requests

app = Flask(__name__)

c = Config('cfg.cfg')
github = Github(c)

def get_labels(labels_loc):
    _, owner, repo = labels_loc.split('/')
    r = requests.get(f'{github.api_url}/{owner}/{repo}/labels')
    labels = r.json()
    for label in labels:
        print(label['name'], label['color'], label['description'])
    return labels

required_labels = get_labels(c.get_repo_with_labels())

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'