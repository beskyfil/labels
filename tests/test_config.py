from labelsync.conf import Config
import pytest
from labelsync.helpers import ConfigError

def test_no_gh_token():
    c = Config("./fixtures/empty.cfg")
    with pytest.raises(ConfigError):
        c.get_github_token() 