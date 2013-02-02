#! /usr/bin/env python
#-*- coding: utf-8 -*-

# ==============================================================================
#                                   IMPORTS
# ==============================================================================

# System imports
from __future__ import print_function
import sys

# Command utils
from datackaton.commands.BaseCommand import BaseCommand
from termcolor import colored

# Database
from py2neo import neo4j
from py2neo import cypher

# ==============================================================================
#                                   COMMAND
# ==============================================================================

class Neo4jCommand(BaseCommand):
    
    help = """
        Tutorial command that : 
        - connects to a neo4j database
        - inserts a couple of nodes and creates relationshops
        - performs a cypher query
        
        Example use :
        python datackaton/commands/Neo4jCommand.py
    """
    
    option_list = BaseCommand.option_list + (
    )
    
    def handle(self, *args, **options):
    
        # ----------------------------------------------------------------------
        # Attach to the graph db instance
        # ----------------------------------------------------------------------
        database = "http://localhost:7474/db/data/"
        print("Connect to database "+database)
        print()
        self.graph_db = neo4j.GraphDatabaseService(database)
        # self.graph_db.clear()
        node_uri_dbpedia_index = self.graph_db.get_or_create_index(neo4j.Node, "node_uri_dbpedia")
        
        # ----------------------------------------------------------------------
        # Import
        # ----------------------------------------------------------------------
        
        cepage_concept = {"uri_dbpedia":"http://fr.wikipedia.org/wiki/C%C3%A9page", "name": "Cépage"}
        cepages = [
            {"uri_dbpedia":"http://fr.dbpedia.org/resource/Couston", "name": "Couston"},
            {"uri_dbpedia":"http://fr.dbpedia.org/resource/Syrah", "name": "Syrah"},
            {"uri_dbpedia":"http://fr.dbpedia.org/resource/Merlot", "name": "Merlot"}
        ]

        # Create nodes and relations
        cepage_concept_node = self.create_safe(cepage_concept, node_uri_dbpedia_index)
        for cepage in cepages:
            cepage_node = self.create_safe(cepage, node_uri_dbpedia_index)
            print("+ Creating link "+colored(cepage['name']+"-[:IS_A]->"+cepage_concept['name'], 'yellow'))
            self.graph_db.get_or_create_relationships((cepage_concept_node, "IS_A", cepage_node))
        print()
            
        # ----------------------------------------------------------------------
        # Report
        # ----------------------------------------------------------------------
        
        # Print all existing nodes
        query = "START n=node(*) RETURN count(*);"
        result = cypher.execute(self.graph_db, query)
        print(str(result[0][0][0])+" nodes")
        
        # Print all existing relations
        query = "START n=node(*) MATCH n-[r]->() RETURN type(r), count(*);"
        results = cypher.execute(self.graph_db, query)
        for relation in results[0]:
            print(str(relation[1])+" "+str(relation[0])+" relations")
        


        
    def create_safe(self, concept, index):
        """
            Thin wrapper designed to safely insert concepts into the graph, 
            with uniqueness of the uri_dbpedia.
        """
        
        concept_node = self.graph_db.get_or_create_indexed_node(index.name, 'uri_dbpedia', concept['uri_dbpedia'])
        if concept_node['metadata']:
            print("+ Creating node "+colored(concept['name'], 'green'))
        else:
            print("+ Updating node "+concept['name'])
        concept_node.update_properties(concept)
            
        return concept_node
        
    
    
if __name__== "__main__" :
    command = Neo4jCommand()
    command.run_from_argv(sys.argv)