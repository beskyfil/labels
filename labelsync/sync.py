import click
from flask import Flask, request
from labelsync.conf import Config
from labelsync.github import Github
from labelsync.gitlab import Gitlab
import requests

@click.command(name='labelsync')
@click.option('-c', '--config-file', type=click.File('r'), help='File with configuration.', required=True)
@click.option('-h', '--host', default="0.0.0.0", show_default=True, type=click.STRING, help='Host to run app on')
@click.option('-p', '--port', default=1234, show_default=True, type=click.INT, help='Port oon which the app will listen.')
def run(config_file, host, port):
    app = Flask(__name__)

    cfg = Config(config_file)
    cfg.check_config()
    github = Github(cfg, name='github', api_url='https://api.github.com/repos')
    gitlab = Gitlab(cfg, name='gitlab', api_url='https://gitlab.com/api/v4/projects')

    @app.route('/github', methods=['POST'])
    def handle_github():
        return github.handle_incoming_hook(request)

    @app.route('/gitlab', methods=['POST'])
    def handle_gitlab():
        return gitlab.handle_incoming_hook(request)

    @app.route('/config', methods=['POST'])
    def handle_config():
        return cfg.handle_incoming_hook(request)

    @app.route('/')
    def hello():
        return 'dummy'

    app.run(host=host, port=port)