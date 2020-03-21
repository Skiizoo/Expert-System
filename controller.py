#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
import argparse
import display
from error import ParseError, SolveError
from parse import Parse
from expertSystem import ExpertSystem


class Controller:

    def __init__(self):
        self.pathToFile = None

    def run(self):
        controller = self
        controller.arg()
        try:
            parser = Parse(controller)
            ExpertSystem(parser)
        except ParseError as e:
            print(e)
        except SolveError as e:
            print(e)

    def arg(self):
        parser = argparse.ArgumentParser(description="resolve logical expression")
        parser.add_argument('pathToFile', help='File to parse')
        parser.add_argument("-d", "--debug", help="display optional information during the process",
                            action="store_true")
        args = parser.parse_args()
        display.debug = args.debug
        self.pathToFile = args.pathToFile
