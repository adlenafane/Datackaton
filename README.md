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


## Install Graph tools

### Install Neo4j

```
mkdir -p /var/db/neo4j
cd /var/db/neo4j
wget http://dist.neo4j.org/neo4j-community-1.9.M04-unix.tar.gz
gunzip neo4j-community-1.9.M04-unix.tar.gz
tar -xf neo4j-community-1.9.M04-unix.tar
cd neo4j-community-1.9.M04
bin/neo4j start
# Go to http://localhost:7474
```

You can follow the tutorial here :
http://www.neo4j.org/learn/cypher

### Install Rabbithole

Rabbithole is a nice GUI for Neo4J. Some help available here :
http://stackoverflow.com/questions/14270730/starting-the-console-with-my-own-graph

```
cd /var/tools
git clone git://github.com/neo4j-contrib/rabbithole.git
cd rabbithole 
mvn assembly:single
java -cp "target/neo4j-console-jar-with-dependencies.jar" org.neo4j.community.console.Console <port> <path-to-local-db> expose
```

For instance, you can set <port> to 7475 and <path-to-local-db> to http://localhost
to access the GUI at http://localhost:7475/.

### Install Python drivers

```
easy_install py2neo
```