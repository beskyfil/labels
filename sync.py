from flask import Flask, escape, request
from conf import Config
from github import Github
import requests

app = Flask(__name__)

c = Config('cfg.cfg')
github = Github(c)

github.update_labels('beskyfil', 'test1')

@app.route('/github', methods=['POST'])
def handle_post():
    return github.handle_incoming_hook(request)

@app.route('/')
def hello():
    return 'dummy'