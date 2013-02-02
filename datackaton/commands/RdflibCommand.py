#! /usr/bin/env python
#-*- coding: utf-8 -*-

# ==============================================================================
#                                   IMPORTS
# ==============================================================================

import sys

from datackaton.commands.BaseCommand import BaseCommand
from optparse import make_option

from datackaton.utils.cache.shortcut import curlRDF

from rdflib import Graph
from rdflib import URIRef

# ==============================================================================
#                                   COMMAND
# ==============================================================================

class RdflibCommand(BaseCommand):
    
    help = """
        Tutorial command that retrieves RDF data from DBpedia.
        
        Example use :
        python datackaton/commands/RdflibCommand.py
    """
    
    option_list = BaseCommand.option_list + (
    )
    
    def handle(self, *args, **options):
    
        # Holder for our data
        g = Graph()
        
        # Find the DBpedia resource equivalent to a wikipedia page
        # http://fr.wikipedia.org/wiki/Elvis_Presley
        urls = [
            "http://dbpedia.org/resource/Elvis_Presley",
            "http://dbpedia.org/resource/Tim_Berners-Lee",
            "http://dbpedia.org/resource/Albert_Einstein",
            "http://dbpedia.org/resource/Margaret_Thatcher"
        ];
        for url in urls:
            print url
            g.parse(data=curlRDF(url), format="application/rdf+xml")

        # Display the number of vertices that were added to the Graph
        print len(g)
        # You can see a list of this data typing directly in your browser
        # http://dbpedia.org/page/Elvis_Presley
        
        for stmt in g.subject_objects(URIRef("http://dbpedia.org/ontology/birthDate")):
            print "the person represented by", str(stmt[0]), "was born on", str(stmt[1])
            
    
    
if __name__== "__main__" :
    command = RdflibCommand()
    command.run_from_argv(sys.argv)