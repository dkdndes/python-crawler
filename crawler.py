#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import requests, pyquery, urlparse
"""crawl to a variable depth looking for a search term"""
try:
    range = xrange
except NameError:
    pass

def crawl(seed, depth, terms):
    """
    crawl from a seed URI to a given depth, looking for search terms.
    yields tuples of uri, term_count, indicating how many of the search 
    terms were found at the yielded uri.
    """
    crawled = set()
    uris = set([seed])
    for level in range(depth):
        new_uris = set()
        for uri in uris:
            if uri in crawled:
                continue
            crawled.add(uri)
            # Get URI contents
            try:
                content = requests.get(uri).content
            except:
                continue
            # Look for the terms
            found = 0
            for term in terms:
                if term in content:
                    found += 1
            if found > 0:
                yield (uri, found, level + 1)
            # Find child URIs, and add them to the new_uris set
            dom = pyquery.PyQuery(content)
            for anchor in dom('a'):
                try:
                    link = anchor.attrib['href']
                except KeyError:
                    continue
                new_uri = urlparse.urljoin(uri, link)
                new_uris.add(new_uri)
        uris = new_uris

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 4:
        print('usage: ' + sys.argv[0] + 
            "start_url crawl_depth term1 [term2 [...]]")
        print('       ' + sys.argv[0] + 
            " http://yahoo.com 5 cute 'fluffy kitties'")
        raise SystemExit

    seed_uri = sys.argv[1]
    crawl_depth = int(sys.argv[2])
    search_terms = sys.argv[3:]

    for uri, count, depth in crawl(seed_uri, crawl_depth, search_terms):
        print(uri)
