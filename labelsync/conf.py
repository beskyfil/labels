import configparser
import os
import requests
from labelsync.helpers import *
import pathlib

class Config():
    """Config class represents configuration of the main configuration repo, 
    it only supports Github repository as storage of configuration of the labels
    """
    def __init__(self, _cfg_file_name):
        """
        :param _cfg_file_name: name of the configuration file
        """
        self.config = configparser.ConfigParser()
        self.config.read(_cfg_file_name.name)
        self.check_config()
        self.secret = self.get_secret()
        self.config_labels = self.get_config_labels()
        self._observers = []

    def bind_to(self, callback):
        """Binds service's update methods to be called whenever config repo changes

        :param callback: callback paramteres is a function, method of each service which updates repositories on given service must be bound to Config class
        """
        print(f'bound {callback.__qualname__}')
        self._observers.append(callback)

    def get_repos_for_service(self, service_name):
        """Returns reposlugs for given service

        :param service_name: string, name of service, currently supported are: github, gitlab
        :return: dictionary with keys 'owner' and 'repo'
        """
        return [{'owner':r.split('/')[1], 'repo':r.split('/')[2]} for r in self.get_repos_to_sync() if r.split('/')[0] == service_name]

    def handle_incoming_hook(self, hook):
        """Handles hook which was received by the app on /config URI, checks integrity of the hook and notifies every observer about the changes

        :param hook: response from github as it was received
        :return: message, status code tuple, this is required by Flask
        """
        msg, code = check_github_hook(hook, self.secret)
        if code != 200:
            return msg, code

        self.config_labels = self.get_config_labels()
        for callback in self._observers:
            print('announcing change')
            callback(hook)
        return 'ok', 200

    def get_config_labels(self):
        """Sends GET request to github API and receives JSON of labels in config repo

        :return: dictionary of labels, keys are names of labels, values are simplified labels which contain only name, color, description attributes
        """
        owner, repo = self.get_repo_with_labels().split('/')
        r = requests.get(f'https://api.github.com/repos/{owner}/{repo}/labels')
        if r.status_code != 200:
            raise HTTPError(f'Error {r.status_code} in GET request: {r.json()["message"]}')
        labels = {}
        for label in r.json():
            labels[label['name']] = {'name':label['name'], 'color':label['color'], 'description':label['description']}
        return labels
    
    def check_config(self):
        """Checks integrity of config file, whether it has all mandatory sections, 
        and if environment variables are set with tokoens for services
        Otherwise particular exception is raised
        """
        if not all(s in ['labels_loc', 'repos', 'services', 'secret'] for s in self.config.sections()):
            raise ConfigError('required fields missing')

    def get_repo_with_labels(self):
        """Reads 'labels_loc' section from config file, which is repo location where labels are

        :return: string with slash-separated reposlug of repo which contains config labels to be synced"""
        return self.config['labels_loc']['l']

    def get_repos_to_sync(self):
        """Reads 'repos' section from config file

        :return: list of slash-separated reposlugs of 
        """
        return [self.config['repos'][r] for r in self.config['repos']]

    def get_secret(self):
        """Reads 'secret' section from the config file, this same secret is used for every webhook
        
        :return: string, secret
        """
        return self.config['secret']['secret']

    def get_github_token(self):
        """Reads env variable or throws exception if its not set

        :return: string, github token
        """
        if not os.getenv('AUTH_CONFIG'):
            raise ConfigError('no AUTH_CONFIG environment variable set')

        return os.environ['AUTH_CONFIG']

    def get_gitlab_token(self):
        """Reads env variable or throws exception if its not set

        :return: string, gitlab token
        """
        if not os.getenv('GITLAB_CONFIG'):
            raise ConfigError('no GITLAB_CONFIG environment variable set')

        return os.environ['GITLAB_CONFIG']
