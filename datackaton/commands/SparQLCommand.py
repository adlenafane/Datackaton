#! /usr/bin/env python
#-*- coding: utf-8 -*-

# ==============================================================================
#                                   IMPORTS
# ==============================================================================

from SPARQLWrapper import SPARQLWrapper, JSON
from datackaton.commands.BaseCommand import BaseCommand

from optparse import make_option
from optparse import OptionParser

import sys


# ==============================================================================
#                                   COMMAND
# ==============================================================================

class SparQLCommand(BaseCommand):
    
    help = """
        Performs a query against a SparQL endpoint. 
        http://sparql-wrapper.sourceforge.net/
        
        Example use :
        python datackaton/commands/SparQLCommand.py
    """
    
    option_list = BaseCommand.option_list + (
        make_option('--show-errors', action='store', dest='show-errors', default=False, help='Prints the bad results', type="int"),
    )
    
    def handle(self, *args, **options):
    
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setQuery("""
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?label
            WHERE { <http://dbpedia.org/resource/Asturias> rdfs:label ?label }
        """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        for result in results["results"]["bindings"]:
            try:
                print(result["label"]["value"])
            except:
                pass
    
    
    
if __name__== "__main__" :
    command = SparQLCommand()
    command.run_from_argv(sys.argv)