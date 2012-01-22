#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys, requests, pyquery, urlparse, time
"""crawl to a variable depth looking for a search term"""
try:
    range = xrange
except NameError:
    pass

if len(sys.argv) < 4:
    print('usage: ' + sys.argv[0] + ' start_url crawl_depth search term')
    print('       ' + sys.argv[0] + ' http://yahoo.com 5 look for me')
    raise SystemExit

seed_uri = sys.argv[1]
crawl_depth = int(sys.argv[2])
search_term = ' '.join(sys.argv[3:])

results = set()
crawled = set() # To eliminate reparsing
uris = set([seed_uri])
for level in range(crawl_depth):
    print(level, len(uris))
    new_uris = set()
    print('-' * len(uris))
    for uri in uris:
        if uri in crawled:
            print('+', end='')
            sys.stdout.flush()
        else:
            print('.', end='')
            sys.stdout.flush()
        if uri in crawled:
            continue
        crawled.add(uri)
        # Get URI contents
        try:
            content = requests.get(uri).content
        except Exception as e:
            continue
        # Search for search_term
        if uri not in results and search_term in content:
            results.add(uri)
        # Find child URIs, and add them to the new_uris set
        d = pyquery.PyQuery(content)
        for anchor in d('a'):
            try:
                link = anchor.attrib['href']
            except KeyError:
                continue
            new_uri = urlparse.urljoin(uri, link)
            new_uris.add(new_uri)
    uris = new_uris
    print()
for result in results:
    print(result)
