#! /usr/bin/env python
#-*- coding: utf-8 -*-

# ==============================================================================
#                                   IMPORTS
# ==============================================================================

from datackaton.utils.cache.SQLiteCache import SQLiteCache

# ==============================================================================
#                                   COMMAND
# ==============================================================================

import urllib2

@SQLiteCache("curlRDF")
def curlRDF(url):
    request = urllib2.Request(url, headers={"Accept" : "application/rdf+xml"})
    return urllib2.urlopen(request, timeout=5).read()
