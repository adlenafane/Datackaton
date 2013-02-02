#! /usr/bin/env python
#-*- coding: utf-8 -*-

# ==============================================================================
#                                   IMPORTS
# ==============================================================================

from optparse import OptionParser
import sys

# ==============================================================================
#                                   COMMAND
# ==============================================================================

class BaseCommand(object):
        
    help = """
        Base command designed to mock the base Django command without requiring
        the entire framework.
    """
    option_list = ()


    def create_parser(self):
        return OptionParser(option_list=self.option_list)
    
    def run_from_argv(self, argv):
        parser = self.create_parser()
        options, args = parser.parse_args(argv)
        self.execute(*args, **options.__dict__)

    def execute(self, *args, **options):
        #self.handle(*args, **options)
        #self.handleRegionmereSousregionAppelation(*args, **options)
        self.getAllVertex(*args, **options)
