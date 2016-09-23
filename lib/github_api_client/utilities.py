import os
import json as JSON

import requests


URL_PREFIX = 'https://api.github.com/'
HEADERS = dict(Accept='application/vnd.github.v3+json')

if 'GITHUB_TOKEN' in os.environ:
    HEADERS['Authorization'] = "token %s" % os.environ['GITHUB_TOKEN']

class ResourceNotAvailable(Exception):
    pass

def api(url, verb=None, json=None):
    if json and not verb:
        verb = 'POST'
    elif not verb:
        verb = 'GET'

    if not url.startswith(URL_PREFIX):
        url = URL_PREFIX + url

    kwargs = dict(headers=HEADERS)
    if json:
        kwargs['json'] = json

    return requests.request(verb, url, **kwargs)

def collect_resource(endpoint):
    page = api(endpoint)
    if page.status_code > 399:
        raise ResourceNotAvailable(page.status_code)
    next_ = page.links.get('next', None)
    resource = JSON.loads(page.text)
    while next_:
        page = api(next_['url'])
        next_ = page.links.get('next', None)
        resource.extend(JSON.loads(page.text))
    return resource

def create_label(repo_name, label_name, color):
    return api(URL_PREFIX + 'repos/' + repo_name + '/labels',
               json=dict(name=label_name, color=color))

def get_user_keys(username):
    return api('users/%s/keys' % username)
