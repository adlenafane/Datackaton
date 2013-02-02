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
sudo easy_install -U "rdflib>=3.0.0"
```

## Create cache folders

```
mkdir -p /var/tmp/sqlitecache/
touch /var/tmp/sqlitecache/curlRDF.sqlite
```
