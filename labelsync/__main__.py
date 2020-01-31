from .sync import run
from labelsync.conf import Config
from labelsync.github import Github
from labelsync.gitlab import Gitlab

run(prog_name='labelsync')