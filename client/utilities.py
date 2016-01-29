# -*- mode: python -*-
# vi: set ft=python :
import os
import json

import requests


class ResourceNotAvailable(Exception):
    pass


url_prefix = 'https://api.github.com/'
github_access_token = os.environ['GITHUB_ACCESS_TOKEN']
headers = dict(Accept='application/vnd.github.v3+json',
               Authorization="token %s" % github_access_token)

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
    api(url_prefix + 'repos/' + repo_name + '/labels',
        json=dict(name=label_name, color=color))

def copy_labels(source_repo_name, target_repo_name):
    for label in collect_resource('repos/' + source_repo_name + '/labels'):
        create_label(target_repo_name, label['name'], label['color'])
