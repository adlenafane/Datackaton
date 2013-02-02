#! /usr/bin/env python
#-*- coding: utf-8 -*-

# ==============================================================================
#                                   IMPORTS
# ==============================================================================

import sys

from datackaton.commands.BaseCommand import BaseCommand

from rdflib import Graph
from rdflib import URIRef

# ==============================================================================
#                                   COMMAND
# ==============================================================================

class OntologyCommand(BaseCommand):
    
    help = """
        Tutorial command that : 
        - loads retrieves RDF data from a local file
        - prints all objects
        - performs an example SparQL query
        
        Example use :
        python datackaton/commands/OntologyCommand.py --file
    """
    
    option_list = BaseCommand.option_list + (
        
    )
    
    def handle(self, *args, **options):
    
        # Load a local ontology
        g = Graph()
        g.parse(location='/Users/antoinedurieux/Desktop/food.owl')

        # Display the number of vertices that were added to the Graph
        print len(g)
        # You can see a list of this data typing directly in your browser
        # http://dbpedia.org/page/Elvis_Presley
        
        # The graph basicaly stores all the triplets, and we can iterate over them :
        # Iterate over triples in store and print them out.
        for subj, pred, obj in g:
            print subj, '->', pred, '->', obj
            
        # Print all nameSingular relations :
        for subj, pred, obj in g:
            if pred == URIRef('http://chefjerome.com/ontology/food.owl#OWLAnnotationProperty_nameSingular'):
                print obj
        
        # Similar, but with a SparQL query
        query = """
            SELECT ?s ?p ?o 
            WHERE { 
                ?s <http://chefjerome.com/ontology/food.owl#OWLAnnotationProperty_nameSingular> ?o. 
            }
        """ % uri
        results = g.query(query)
        print len(results)
        for result in results:
            print result
        
                
            
    
    
if __name__== "__main__" :
    command = OntologyCommand()
    command.run_from_argv(sys.argv)