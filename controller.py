#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
import argparse
import sys
from error import Error, ParseError
from parse import Parse
from expertSystem import ExpertSystem


class Controller:

	def __init__(self):
		self.debug = False
		self.pathToFile = None

	def run(self):
		controller = self
		controller.arg()
		parser = Parse(controller)
		ExpertSystem(parser)

	def arg(self):
		parser = argparse.ArgumentParser(description="resolve logical expression")
		parser.add_argument('pathToFile', help='File to parse')
		parser.add_argument("-d", "--debug", help="display optional information during the process", action="store_true")
		args = parser.parse_args()
		self.debug = args.debug
		self.pathToFile = args.pathToFile
