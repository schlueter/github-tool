from __future__ import print_function

import os
import json

import requests


class ResourceNotAvailable(Exception):
    pass


url_prefix = 'https://api.github.com/'
github_access_token = os.environ['GITHUB_ACCESS_TOKEN']
headers = dict(Accept='application/vnd.github.v3+json',
               Authorization="token %s" % github_access_token)


def api(url, verb='GET'):
    if not url.startswith(url_prefix):
        url = url_prefix + url
    return requests.request(verb, url, headers=headers)

def collect_resource(endpoint):
    page = api(endpoint)
    if page.status_code > 399:
        raise ResourceNotAvailable(page.status_code)
    next_ = page.links['next']
    resource = json.loads(page.text)
    while next_:
        page = api(next_['url'])
        next_ = page.links.get('next', None)
        resource.extend(json.loads(page.text))
    return resource

if __name__ == '__main__':
    from pprint import pprint as pp
    pp(collect_resource('orgs/refinery29/members'))
