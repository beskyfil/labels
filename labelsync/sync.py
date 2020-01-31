from flask import Flask, request
from conf import Config
from github import Github
from gitlab import Gitlab
import requests

app = Flask(__name__)

c = Config('cfg.cfg')
github = Github(c, name='github', api_url='https://api.github.com/repos')
gitlab = Gitlab(c, name='gitlab', api_url='https://gitlab.com/api/v4/projects')

@app.route('/github', methods=['POST'])
def handle_github():
    return github.handle_incoming_hook(request)

@app.route('/gitlab', methods=['POST'])
def handle_gitlab():
    return gitlab.handle_incoming_hook(request)

@app.route('/config', methods=['POST'])
def handle_config():
    return c.handle_incoming_hook(request)

@app.route('/')
def hello():
    return 'dummy'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1234)