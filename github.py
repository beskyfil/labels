class Github:
    def __init__(self, login):
        self.login = login
        self.api_url = 'https://api.github.com/repos/'
        # f'https://api.github.com/repos/{self.reposlug}/issues'