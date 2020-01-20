import configparser

class Config:
    def __init__(self, _cfg_file_name):
        self._cfg_file_name = _cfg_file_name
        self.config = configparser.ConfigParser()
        self.config.read(_cfg_file_name)
        self.check_config()
    
    def check_config(self):
        if not all(s in ['labels', 'repos'] for s in self.config.sections()):
            raise RuntimeError('config error')

    def get_labels_repo(self):
        return self.config['labels']['l']

    def get_repos_to_synch(self):
        return [self.config['repos'][r] for r in self.config['repos']]

c = Config('cfg.cfg')
print(c.get_repos_to_synch())