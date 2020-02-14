import argparse
from step import Step
from error import ParseError
from rule import Rule
import re


class Parse:

	def __init__(self, controller):
		self.controller = controller
		self.rules = []
		self.facts = []
		self.queries = []
		self.get_params()

	def get_params(self):
		with open(self.controller.pathToFile) as f:
			current_step = Step.rules
			file = [x for x in re.sub(r'(#.*)|([\t ])', '', f.read()).split('\n') if x]

			for i, line in enumerate(file):
				if current_step is None:
					raise ParseError('stepParse == None')
				if current_step is Step.rules:
					if self.valid_rule(line, i):
						self.rules += [Rule(line)]
					else:
						current_step = next(current_step)
				if current_step is Step.facts:
					if not self.valid_fact(line, i):
						raise ParseError("invalid facts")
					self.facts = re.sub(r'=', '', line)
					current_step = next(current_step)
				elif current_step is Step.queries:
					if not self.valid_query(line, i):
						raise ParseError("invalid queries")
					self.queries = re.sub(r'\?', '', line)
					current_step = next(current_step)

	def valid_rule(self, line, i) -> bool:
		op = ['+', '|', '^']
		par = ['(', ')']

		if self.valid_fact(line, i):
			return False
		if self.valid_query(line, i):
			raise ParseError('Facts missing')
		rules = line.split('=>')
		if len(rules) != 2:
			raise ParseError("Rules isn't well computed at line " + str(i))
		for rule in rules:
			prev = None
			count = 0
			for j, char in enumerate(rule):
				if self.is_upper_alpha(char) and self.is_upper_alpha(prev):
					raise ParseError("Two characters A-Z are following at line " + str(i))
				elif char not in op and char not in par and not self.is_upper_alpha(char) and char != '!':
					raise ParseError("Unknown character at line " + str(i))
				elif char == par[0]:
					count += 1
					if self.is_upper_alpha(prev):
						raise ParseError("No operator before '(' at line " + str(i))
				elif char == par[1]:
					if count <= 0 or (not self.is_upper_alpha(prev) and prev != par[1]):
						raise ParseError("Closed parenthesis not open at line " + str(i))
					count -= 1
				elif char in op and ((not self.is_upper_alpha(prev) and not prev == par[1]) or j == len(line)):
					raise ParseError("Incorrect character before op at line " + str(i))
				elif char == '!' and (self.is_upper_alpha(prev) or j == len(rule)):
					raise ParseError("Incorrect character before negation at line " + str(i))
				prev = char
		return True

	@staticmethod
	def valid_fact(line, i) -> bool:
		if re.match(r'^=(?!.*?(.).*?\1)[A-Z]*$', line):
			return True
		return False

	@staticmethod
	def valid_query(line, i) -> bool:
		if re.match(r'^\?(?!.*?(.).*?\1)[A-Z]*$', line):
			return True
		return False

	@staticmethod
	def is_upper_alpha(char):
		return char is not None and char.isalpha() and char.isupper()
