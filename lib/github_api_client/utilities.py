"""
Utilities for interacting with GitHub's api
"""
import os
import json as JSON
from typing import Literal, Optional, Union

import requests


URL_PREFIX = 'https://api.github.com/'
ACCEPT_HEADERS = [
    # Current version of API
    'application/vnd.github.v3+json',
    # Protected branches required number of approving pull requests
    'application/vnd.github.luke-cage-preview+json',
    # Protected branches signed commits requirement
    'application/vnd.github.zzzax-preview+json'
]
HEADERS = dict(accept=','.join(ACCEPT_HEADERS))

if 'GITHUB_TOKEN' in os.environ:
    HEADERS['Authorization'] = "token %s" % os.environ['GITHUB_TOKEN']

HTTPVerbsType = Optional[Literal['GET', 'POST', 'PUT']]
JSONType = Optional[Union[str, int, float, bool, dict, list]]


class ResourceNotAvailable(Exception):
    """
    Exception indicating that the resource is not available
    """


def api(
        url: str,
        verb: HTTPVerbsType = None,
        json: JSONType = None,
        headers: Optional[dict] = None
        ):
    """
    API call method
    """

    if json and not verb:
        verb = 'POST'
    elif not verb:
        verb = 'GET'

    if not url.startswith(URL_PREFIX):
        url = URL_PREFIX + url

    kwargs = dict(headers={**HEADERS, **(headers or {})})
    if json:
        kwargs['json'] = json

    return requests.request(verb, url, **kwargs)


def collect_resource(endpoint: str):
    """
    For resources which may have multiple pages of content, collect all pages
    into a list.
    """
    page = api(endpoint)
    if page.status_code > 399:
        raise ResourceNotAvailable(
            f"requesting {endpoint} resulted in {page.status_code}"
        )
    next_ = page.links.get('next', None)
    resource = JSON.loads(page.text)
    while next_:
        page = api(next_['url'])
        next_ = page.links.get('next', None)
        resource.extend(JSON.loads(page.text))
    return resource


def create_label(repo_name: str, label_name: str, color: str):
    """
    Shortcut to create a label (for issues) on a repository
    """
    return api('repos/' + repo_name + '/labels',
               json=dict(name=label_name, color=color))


def update_label(
        repo_name: str,
        current_name: str,
        new_name: Optional[str] = None,
        new_color: Optional[str] = None,
        new_description: Optional[str] = None
        ):
    """
    Shortcut to update a label (for issues) on a repository
    """
    preview_accept_header = 'application/vnd.github.symmetra-preview+json'
    payload = dict()
    if new_name:
        payload['name'] = new_name
    if new_color:
        payload['color'] = new_color
    if new_description:
        payload['description'] = new_description
    return api('repos/' + repo_name + '/labels/' + current_name,
               json=payload,
               headers=dict(Accept=preview_accept_header))


def get_user_keys(username: str):
    """
    Shortcut to get a user's public keys
    """
    return api('users/%s/keys' % username)
