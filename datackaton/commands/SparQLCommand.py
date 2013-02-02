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
        python datackaton/commands/SparQLCommand.py --region=1
    """
    
    option_list = BaseCommand.option_list + (
        make_option('--region', action='store', dest='region', default=False, help='Loads the list of regions', type="int"),
        make_option('--cepage', action='store', dest='cepage', default=False, help='Loads the list of cepages', type="int"),
    )
    
    
    def handle(self, *args, **options):
        """
            Configures the SparQL endpoint to tap into fr.dbpedia.
            Routes the request to the appropriate function.
        """
    
        self.sparql = SPARQLWrapper("http://fr.dbpedia.org/sparql")
        self.sparql.setReturnFormat(JSON)
        
        if options['region']:
            self.load_region()
        
        if options['cepage']:
            self.load_cepage()
        
        
    def load_cepage(self):
        """
            Retrieves the cepages based on their template.
        """
        
        self.sparql.setQuery(u"""
            PREFIX dbo: <http://dbpedia.org/ontology/> 
            PREFIX res: <http://dbpedia.org/resource/> 
            PREFIX dbp: <http://fr.dbpedia.org/property/> 
            SELECT ?uri
            WHERE { 
                ?uri prop-fr:wikiPageUsesTemplate <http://fr.dbpedia.org/resource/Modèle:Infobox_Cépage> .
            }
        """)
        
        results = self.sparql.query().convert()
        for result in results["results"]["bindings"]:
            print(result["uri"]["value"])
        print len(results)
        
        return results
        
        
    def load_region(self):
        """
            Retrieves the regions based on their template.
        """
        
        self.sparql.setQuery(u"""
            PREFIX dbo: <http://dbpedia.org/ontology/> 
            PREFIX res: <http://dbpedia.org/resource/> 
            PREFIX dbp: <http://fr.dbpedia.org/property/> 
            SELECT ?uri
            WHERE { 
                ?uri prop-fr:wikiPageUsesTemplate <http://fr.dbpedia.org/resource/Modèle:Infobox_Région_viticole> .
            }
        """)
        
        results = self.sparql.query().convert()
        for result in results["results"]["bindings"]:
            print(result["uri"]["value"])
        print len(results)
    
        return results
    
    
    
    
if __name__== "__main__" :
    command = SparQLCommand()
    command.run_from_argv(sys.argv)