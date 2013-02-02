Datackaton
==========

# How to install ?

## Install dependencies

```
# SparQL wrapper is a connector to SparQL endpoints
# http://sparql-wrapper.sourceforge.net/
easy_install SPARQLWrapper

# Rdflib is a parser for RDF resources
# https://rdflib.readthedocs.org/en/latest/
easy_install -U "rdflib>=3.0.0"
easy_install http://cheeseshop.python.org/packages/source/p/pyparsing/pyparsing-1.5.5.tar.gz
easy_install rdfextras
```

## Create cache folders

```
mkdir -p /var/tmp/sqlitecache/
touch /var/tmp/sqlitecache/curlRDF.sqlite
```
