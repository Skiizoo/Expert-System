import argparse
from utils import exitWithErrors
from step import Step
import re


class Parse:

	def __init__(self, controller):
		self.controller = controller
		self.rules = []
		self.facts = []
		self.queries = []
		self.getParams()

	def getparams(self):
		try:
			with open(self.file) as f:
				step_parse = Step.expr
				file = [x for x in re.sub(r'(#.*)|([\t ])', '', f.read()).split('\n') if x]
				for line in file:
					if step_parse is Step.expr:
						if True:  # if valid rules
							self.rules += [Rule(line)]
						else:
							step_parse = next(step_parse)
					if step_parse is Step.facts:
						if facts := True:  # if valid fact
							step_parse = next(step_parse)
						else:
							raise Error()
					if step_parse is Step.queries:  # if valid queries
						if queries := True:
							step_parse = next(step_parse)
							continue
						else:
							raise Error()
					if step_parse is None:
						raise Error('Error=', 'Message')
		except Error as error:
			print(error.message)
			exit()

	def valid_rules(self, rules, i):
		prev = None
		count = 0
		op = ['+', '|', '^']
		par = ['(', ')']

		for j, char in enumerate(rules):
			if self.is_upper_alpha(char) and self.is_upper_alpha(prev):
				exitWithErrors("Wrong format at line " + str(i))
			elif char not in op and char not in par and not self.is_upper_alpha(char) and char != '!':
				exitWithErrors("Wrong format at line " + str(i))
			elif char == par[0]:
				count += 1
				if self.is_upper_alpha(prev):
					exitWithErrors("Wrong format at line " + str(i))
			elif char == par[1]:
				if count <= 0 or (not self.is_upper_alpha(prev) and prev != par[1]):
					exitWithErrors("Wrong format at line " + str(i))
				count -= 1
			elif char in op and ((not self.is_upper_alpha(prev) and not prev == par[1]) or j == len(rules)):
				exitWithErrors("Wrong format at line " + str(i))
			elif char == '!' and (self.is_upper_alpha(prev) or j == len(rules)):
				exitWithErrors("Wrong format at line " + str(i))

			prev = char

	@staticmethod
	def is_upper_alpha(char):
		return char is not None and char.isalpha() and char.isupper()