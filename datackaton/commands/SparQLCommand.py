#! /usr/bin/env python
#-*- coding: utf-8 -*-

# ==============================================================================
#                                   IMPORTS
# ==============================================================================

from SPARQLWrapper import SPARQLWrapper, JSON
from datackaton.commands.BaseCommand import BaseCommand
import pprint, cPickle
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
            { 
                ?appelation prop-fr:wikiPageUsesTemplate <http://fr.dbpedia.org/resource/Modèle:Infobox_Région_viticole> .
                ?appelation prop-fr:cépages ?cepages
            } 
            }
        """)
        sparql.setReturnFormat(JSON)
        
        results = sparql.query().convert()
        for result in results["results"]["bindings"]:
            print(result["appelation"]["value"], result["cepages"]["value"])
    
    def handleRegionmereSousregionAppelation(self, *args, **options):
    
        sparql = SPARQLWrapper("http://fr.dbpedia.org/sparql")
        sparql.setQuery(u"""
            PREFIX dbo: <http://dbpedia.org/ontology/> 
            PREFIX res: <http://dbpedia.org/resource/> 
            PREFIX dbp: <http://fr.dbpedia.org/property/> 
            SELECT ?x ?mere ?sous ?appelation
            WHERE { 
            { 
                ?x prop-fr:wikiPageUsesTemplate <http://fr.dbpedia.org/resource/Modèle:Infobox_Région_viticole> .
                ?x prop-fr:régionMère ?mere .
                ?x prop-fr:sousRégions ?sous .
                ?x prop-fr:appellations ?appelation
            } 
            }
        """)
        sparql.setReturnFormat(JSON)
         
        results = sparql.query().convert()
        for result in results["results"]["bindings"]:
            print(result['mere']['value'], result["sous"]["value"], result['appelation']['value'])

    def getAllVertex(self, *args, **options):

        listOfPossibleVertex = ('année', 'appellations', 'climat', 'cépages', 'densité', 'localisation', 'légende', \
                                 'nom', 'rendement', 'régionMère', 'sousRégions', 'typeappellation', 'vins', 'subject', 'label')
        listOfPosssibleEdges = (u'prop-fr:année', u'prop-fr:appellations', u'prop-fr:climat', u'prop-fr:cépages', \
                                 u'prop-fr:densité', u'prop-fr:localisation', u'prop-fr:légende', u'prop-fr:nom', \
                                u'prop-fr:rendement', u'prop-fr:régionMère', u'prop-fr:sousRégions', \
                                u'prop-fr:typeappellation', u'prop-fr:vins', u'dcterms:subject', u'rdfs:label')
        dicOfAllVertex = {}
        for i in range(len(listOfPossibleVertex)):
            node = listOfPossibleVertex[i]
            edge = listOfPosssibleEdges[i]
            print i, node
            sparql = SPARQLWrapper("http://fr.dbpedia.org/sparql")
            sparql.setQuery(u"""
                PREFIX dbo: <http://dbpedia.org/ontology/> 
                PREFIX res: <http://dbpedia.org/resource/> 
                PREFIX dbp: <http://fr.dbpedia.org/property/> 
                SELECT ?x ?y
                WHERE { 
                { 
                    ?x prop-fr:wikiPageUsesTemplate <http://fr.dbpedia.org/resource/Modèle:Infobox_Région_viticole> .
                    ?x """ + edge + """ ?y
                } 
                }
            """)
            sparql.setReturnFormat(JSON)
            dicOfAllVertex[node] = []
            results = sparql.query().convert()
            for result in results["results"]["bindings"]:
                dicOfAllVertex[node].append(result['y']['value'])
            dicOfAllVertex[node] = set(dicOfAllVertex[node])
        pprint.pprint(dicOfAllVertex)
        with open('rawVertex.txt', 'wb') as fp:
            cPickle.dump(dicOfAllVertex, fp)

    def getAppelationList(self, *args, **options):
        appelationList = []
        sparql = SPARQLWrapper("http://fr.dbpedia.org/sparql")
        sparql.setQuery(u"""
            PREFIX dbo: <http://dbpedia.org/ontology/> 
            PREFIX res: <http://dbpedia.org/resource/> 
            PREFIX dbp: <http://fr.dbpedia.org/property/> 
            SELECT ?appelation
            WHERE { 
            { 
                ?x prop-fr:wikiPageUsesTemplate <http://fr.dbpedia.org/resource/Modèle:Infobox_Région_viticole> .
                ?x prop-fr:appellations ?appelation
                FILTER regex(?appelation, "^http://")
            } 
            }
        """)
        sparql.setReturnFormat(JSON)
     
        results = sparql.query().convert()
        for result in results["results"]["bindings"]:
            appelationList.append(result['appelation']['value'])
        appelationList = set(appelationList)
        pprint.pprint(appelationList)


if __name__== "__main__" :
    command = SparQLCommand()
    command.run_from_argv(sys.argv) 