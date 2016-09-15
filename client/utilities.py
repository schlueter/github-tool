import os
import json

import requests


url_prefix = 'https://api.github.com/'
headers = dict(Accept='application/vnd.github.v3+json')

if 'GITHUB_TOKEN' in os.environ:
    headers['Authorization'] = "token %s" % os.environ['GITHUB_TOKEN']
else:
    # TODO make the api interaction display the api limit blocker
    pass

class ResourceNotAvailable(Exception):
    pass

def api(url, verb=None, json=None):
    if json and not verb:
        verb = 'POST'
    elif not verb:
        verb = 'GET'

    if not url.startswith(url_prefix):
        url = url_prefix + url

    kwargs = dict(headers=headers)
    if json:
        kwargs['json'] = json

    return requests.request(verb, url, **kwargs)

def collect_resource(endpoint):
    page = api(endpoint)
    if page.status_code > 399:
        raise ResourceNotAvailable(page.status_code)
    next_ = page.links.get('next', None)
    resource = json.loads(page.text)
    while next_:
        page = api(next_['url'])
        next_ = page.links.get('next', None)
        resource.extend(json.loads(page.text))
    return resource

def create_label(repo_name, label_name, color):
    return api(url_prefix + 'repos/' + repo_name + '/labels',
        json=dict(name=label_name, color=color))

def copy_labels(source_repo_name, target_repo_name):
    return [create_label(target_repo_name, label['name'], label['color']) for
        label in collect_resource('repos/' + source_repo_name + '/labels')]

def get_user_keys(username):
    return api('users/%s/keys' % username)
