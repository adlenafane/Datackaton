#! /usr/bin/env python
#-*- coding: utf-8 -*-

# ==========================================================================
# 
# class FileSystemCache(AbstractCache):
# 
# This is a cache manager system designed to be used seamlessly through an 
# annotation system.
#
# ==========================================================================

# String manipulation imports
import hashlib
# File system imports
import os
import sys
# DB imports
from sqlite3 import dbapi2 as sqlite
# Abstract class extend :
from AbstractCache import AbstractCache



class SQLiteCache(AbstractCache):
    """
        Cache stored in an SQLite database.
    """
    
    def __init__(self,cachePath):
        """
            Initializes the SQLLiteCache with a path and a compression
            setting.
        """    
        self.cursor = None
        self.cachePath = "/var/tmp/sqlitecache/"+cachePath+".sqlite"
        self.createSafe(self.cachePath)
        self.compress = True


    def __call__(self, functionToMemoize):
        """ 
            Decorator function : allows us to attach the decorator to the function.
        """
        def memoized_call(*args):

            # Check there is at least one argument
            assert args
            # Check there is no more than one argument (current limitation)
            if len(args) != 1:
                raise ValueError("Caching more than one arg is not implemented.")

            # Compute the location of the cache
            # Directly stored in the DB
            
            # If a cached version exist
            v = self.get(functionToMemoize.__name__,args[0])

            if v:
                # print(functionToMemoize.__name__+" computed from cache.")
                return v[0]
            else:
                # print("Caching "+functionToMemoize.__name__)
                result = functionToMemoize(*args)
                self.put(functionToMemoize.__name__,args[0],result)
                return result

        # Return this function so the decorator can replace the old one
        return memoized_call

    
    def createSafe(self, path):
        """
            Creates a table to store the calls of the given function if not present.
        """
        if not os.path.exists(path):
            if "/" in path and path != "/" :
                self.createSafe(os.path.dirname(path))
            os.mkdir(path)
        # print(self.cachePath)
        self.conn = sqlite.connect(self.cachePath)
        self.cursor = self.conn.cursor()
        self.cursor.execute( "CREATE TABLE IF NOT EXISTS cache (key VARCHAR PRIMARY KEY ON CONFLICT REPLACE, value VARCHAR)")
        return True

            
    def get(self, functionName, key):
        """
            Returns the cached value.
        """
        self.cursor.execute("SELECT value FROM cache WHERE key=?",(key,))
        val = list(self.cursor)    
        if val:
            if self.compress:
                return [self.unmash(val[0][0])]
            else:
                return [val[0][0]]
        else:
            return []

    def put(self, functionName, key, value):
        """
            Stores the cached value to the given path.
        """
        if self.compress:
            value = self.mash(value)
        self.cursor.execute("INSERT INTO cache VALUES(?,?)",(key,value,))
        self.conn.commit()
        return value

    
    def clear(self, functionName, args=[]):
        """
            Deletes the cache for a given function
        """
        self.cursor.execute("DELETE FROM cache",(key,value,))
        self.conn.commit()
        return True




if __name__== "__main__" :
    
    import urllib2
    
    # Define a function to cache
    @SQLiteCache("functionToCache3")
    def functionToCache3(url):
        return urllib2.urlopen(url, timeout=5).read()
    
    @SQLiteCache("functionToCache2")
    def functionToCache2(url):
        return urllib2.urlopen(url, timeout=5).read()
    
    
    # Clear cache for a range of values
    # cache = FileSystemCache()
    # cache.clear("functionToCache","*http://www.marmiton.org/")
    
    # Test the caching system
    functionToCache3("http://www.marmiton.org/recettes/recette_salade-d-endives-des-gourmands_27660.aspx")
    functionToCache3("http://www.marmiton.org/recettes/recette_lasagnes-aux-poireaux-et-au-saumon_13332.aspx")
    functionToCache3("http://www.marmiton.org/recettes/recette_salade-d-endives-des-gourmands_27660.aspx")

    functionToCache2("http://www.marmiton.org/recettes/recette_salade-d-endives-des-gourmands_27660.aspx")
    functionToCache2("http://www.marmiton.org/recettes/recette_lasagnes-aux-poireaux-et-au-saumon_13332.aspx")
    functionToCache2("http://www.marmiton.org/recettes/recette_salade-d-endives-des-gourmands_27660.aspx")
