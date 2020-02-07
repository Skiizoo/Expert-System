#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import sys
from parse import Parse
from expertSystem import ExpertSystem

class Controller:

    def __init__(self):
        self.parse = Parse(sys.argv)

    def run(self):
        self.parse.getParams()
        ExpertSystem(self.parse.rules, self.parse.facts, self.parse.queries)

