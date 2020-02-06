
import pytest
from labelsync.helpers import ConfigError
import os
import pathlib
from tests.helpers import fl, FIXTURES_PATH, create_cfg_env

def test_no_gh_token():
    c = create_cfg_env('empty.cfg')

    gh = None
    if os.getenv('AUTH_CONFIG'):
        gh = os.getenv('AUTH_CONFIG')
    
    del os.environ['AUTH_CONFIG']

    with pytest.raises(ConfigError):
        c.get_github_token() 

    if gh:
        os.environ['AUTH_CONFIG'] = gh

def test_no_gl_token():
    c = create_cfg_env('empty.cfg')

    gl = None
    if os.getenv('GITLAB_CONFIG'):
        gl = os.getenv('GITLAB_CONFIG')
    
    del os.environ['GITLAB_CONFIG']

    with pytest.raises(ConfigError):
        c.get_gitlab_token() 

    if gl:
        os.environ['GITLAB_CONFIG'] = gl

def test_empty_config():
    c = create_cfg_env('empty.cfg')
    with pytest.raises(ConfigError):
        c.check_config() 

def test_good_config():
    c = create_cfg_env('good.cfg')
    assert c.check_config() == 0