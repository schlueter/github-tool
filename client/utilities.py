from __future__ import print_function

import os
import json
import re

import requests


class ResourceNotAvailable(Exception):
    pass

github_access_token = os.environ['GITHUB_ACCESS_TOKEN']

headers = dict(Accept='application/vnd.github.v3+json',
               Authorization="token %s" % os.environ['GITHUB_ACCESS_TOKEN'])
url_prefix = 'https://api.github.com/'


def clean_rel(rel_string):
    return re.findall('(?<=rel\=\").*(?=\")', rel_string).pop()

def clean_url(url):
    return url.strip('<> ')

def api(url, verb='GET'):
    if not url.startswith(url_prefix):
        url = url_prefix + url
    return requests.request(verb, url, headers=headers)

def parse_links(link):
    links = dict([(clean_rel(i[1]), clean_url(i[0])) for i in
                map(lambda x: x.split(';'), link.split(','))])

    return links.get('next', None), links.get('last')

def collect_resource(endpoint):
    page = api(endpoint)
    if page.status_code > 399:
        raise ResourceNotAvailable(page.status_code)
    next_, last_ = parse_links(page.headers['link'])
    resource = json.loads(page.text)
    last_page = False
    while next_:
        page = api(next_)
        next_, last_ = parse_links(page.headers['link'])
        resource.extend(json.loads(page.text))
    return resource

if __name__ == '__main__':
    from pprint import pprint as pp
    pp(collect_resource('orgs/refinery29/members'))
