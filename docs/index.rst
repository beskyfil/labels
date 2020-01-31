.. labelsync documentation master file, created by
   sphinx-quickstart on Tue Jan 28 16:34:17 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to labelsync's documentation!
=====================================

What it does
--------------
This web application synchronizes defined labels among your repositories on different git-based platforms for version managing (currently only GitHub and GitLab are supported).

Defined labels, which you want to ensure they exist, have to be defined in GitHub public repository. These labels are then populated by the app to each of desired repositories.

Whenever you make change to config repository, these changes will immediately take effect in all the synchronized repositories. If you change label setting in one particular repository, which are in conflict with config repo, these changes will be reverted instantly back to defined default. Last aforementioned functionality is currently only supported for GitHub repos, since GitLab does not provide necessary webhooking for labels.

Setup
-------------
* It's necessary that you create webhooks manually for each repo you wish to keep synchronized.

* Set environment variables with tokens, `AUTH_CONFIG=<token>` for GitHub and `GITLAB_CONFIG=<token>` and GitLab.

* Install requiremets `Flask`, `requests` and `click`,  `python -m pip install -r requirements.txt`

* Run `python setup.py sdist` to generate distro then install it `python -m pip install ...`

* Set `cfg.cfg` config file accordingly (self-explanatory format).

* Run `python -m labelsync -c <cfg_file> --host <hostname> --port <port>`

Implementing your own service
-----------------------------
You will have to extend Service class and implement all methods. Then in `sync.py` add Flask route for handling webhooks of your service.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
