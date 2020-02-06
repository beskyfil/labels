import pytest
from labelsync.github import Github
from labelsync.helpers import HTTPError
from tests.helpers import fl, FIXTURES_PATH, create_cfg_env, get_labels

c = create_cfg_env('good.cfg')
github = Github(c, name='github', api_url='https://api.github.com/repos')

label = {
        'name':'blabla',
        'color':'aa11bb',
        'description':'whatever'
    }

label_bug = {
        'name':'bug',
        'color':'d73a4a',
        'description':'Something isn\'t working'
    }

label_new_bug = {
        'name':'ERROR',
        'color':'ffffff',
        'description':'ERROR'
    }

def test_create_label():
    labels_before = get_labels('beskyfil', 'testing_repo')
    num_labels_before = len(labels_before)

    github.create_label('beskyfil', 'testing_repo', label)

    labels_after = get_labels('beskyfil', 'testing_repo')
    num_labels_after = len(labels_after)

    assert num_labels_before == num_labels_after - 1
    assert 'blabla' not in labels_before
    assert 'blabla' in labels_after

def test_delete_label():
    labels_before = get_labels('beskyfil', 'testing_repo')
    num_labels_before = len(labels_before)

    github.delete_label('beskyfil', 'testing_repo', label['name'])

    labels_after = get_labels('beskyfil', 'testing_repo')
    num_labels_after = len(labels_after)

    assert num_labels_before == num_labels_after + 1
    assert 'blabla' in labels_before
    assert 'blabla' not in labels_after

def test_edit_label():
    labels_before = get_labels('beskyfil', 'testing_repo')
    num_labels_before = len(labels_before)

    github.edit_label('beskyfil', 'testing_repo', label_new_bug, 'bug')

    labels_after = get_labels('beskyfil', 'testing_repo')
    num_labels_after = len(labels_after)

    assert num_labels_before == num_labels_after
    assert 'bug' in labels_before
    assert 'bug' not in labels_after
    assert 'ERROR' in labels_after
    assert 'ERROR' not in labels_before

    #revert
    github.edit_label('beskyfil', 'testing_repo', label_bug, 'ERROR')
