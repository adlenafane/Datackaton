#! /usr/bin/env python
#-*- coding: utf-8 -*-

# ==============================================================================
#                                   IMPORTS
# ==============================================================================

from SPARQLWrapper import SPARQLWrapper, JSON
from datackaton.commands.BaseCommand import BaseCommand

from optparse import make_option

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
    
        sparql = SPARQLWrapper("http://fr.dbpedia.org/sparql")
        sparql.setQuery(u"""
            PREFIX dbo: <http://dbpedia.org/ontology/> 
            PREFIX res: <http://dbpedia.org/resource/> 
            PREFIX dbp: <http://fr.dbpedia.org/property/> 
            SELECT ?appelation ?cepages
            WHERE { 
                ?appelation prop-fr:wikiPageUsesTemplate <http://fr.dbpedia.org/resource/Modèle:Infobox_Région_viticole> .
                ?appelation prop-fr:cépages ?cepages
            }
        """)
        sparql.setReturnFormat(JSON)
        
        results = sparql.query().convert()
        for result in results["results"]["bindings"]:
            print(result["appelation"]["value"], result["cepages"]["value"])
    
    
    
if __name__== "__main__" :
    command = SparQLCommand()
    command.run_from_argv(sys.argv)