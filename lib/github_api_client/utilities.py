import os
import json as JSON

import requests


URL_PREFIX = 'https://api.github.com/'
HEADERS = dict(Accept='application/vnd.github.v3+json')

if 'GITHUB_TOKEN' in os.environ:
    HEADERS['Authorization'] = "token %s" % os.environ['GITHUB_TOKEN']


class ResourceNotAvailable(Exception):
    pass


def api(url, verb=None, json=None, headers={}):
    if json and not verb:
        verb = 'POST'
    elif not verb:
        verb = 'GET'

    if not url.startswith(URL_PREFIX):
        url = URL_PREFIX + url

    kwargs = dict(headers={**HEADERS, **headers})
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
    return api('repos/' + repo_name + '/labels',
               json=dict(name=label_name, color=color))


def update_label(repo_name, current_name, new_name=None, new_color=None, new_description=None):
    payload = dict()
    if new_name:
        payload['name'] = new_name
    if new_color:
        payload['color'] = new_color
    if new_description:
        payload['description'] = new_description
    return api('repos/' + repo_name + '/labels/' + current_name,
               json=payload,
               headers=dict(Accept='application/vnd.github.symmetra-preview+json'))


def get_user_keys(username):
    return api(f"users/{username}/keys")
