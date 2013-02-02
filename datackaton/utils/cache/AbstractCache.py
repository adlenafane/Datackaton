#! /usr/bin/env python
#-*- coding: utf-8 -*-


# ==========================================================================
# 
# class AbstractCache:
# 
# This is a base class for our cache systems.
#
# ==========================================================================

import urlparse
# Compression
import cPickle
import bz2
import base64

class AbstractCache:

    @staticmethod
    def domain(url):
        """ 
            Returns the domain of an url
            >>> domain( "http://lol.com/plop" )
            'lol.com'
            >>> domain( "ftp://ii:80/lol" )
            'ii'
        """
        return urlparse.urlparse(url)[1].split(':')[0]

    @staticmethod
    def mash(arg):
        s = cPickle.dumps(arg)
        s = bz2.compress(s)
        s = base64.b64encode(s)
        return s

    @staticmethod
    def unmash(arg):
        s = base64.b64decode(arg)
        s = bz2.decompress(s)
        s = cPickle.loads(s)
        return s

    def __init__(self,cachePath): abstract
    def __call__(self, functionToMemoize): abstract

    def createSafe(self,path): abstract
    def put(self, functionName, key, value): abstract
    def get(self, functionName, key): abstract
    def clear(self, functionName, args): abstract
