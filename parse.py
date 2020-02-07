import argparse
from utils import exitWithErrors

class Parse:

	def __init__(self, argv):
		self.file = ""
		self.rules = []
		self.facts = []
		self.queries = []

		parser = argparse.ArgumentParser(description="resolve logical expression")
		parser.add_argument('pathToFile', help='File to parse')
		args = parser.parse_args()
		self.file = args.pathToFile

	def getParams(self):

		try:
			with open(self.file) as f:
				lines = f.readlines()

				for i, line in enumerate(lines):
					line = line.replace(' ', '').replace('\n', '')
					#ATTENTION SI MAUVAIS ORDRE
					#ATTENTION SI ESPACE ENTRE FACTS/QUERIES
					#ATTENTION SI PLUSIEURS FACTS/QUERIES
					#ATTENTION SI RULES NON VALIDES
					#ATTENTION SI QUERIES/FACTS NON VALIDES (!= [A-Z])
					if '#' in line:
						line = line.split('#')[0]
					if '=>' in line:
						rule = line.split('=>')
						self.validRules(rule[0], i)
						self.validRules(rule[1], i)
						self.rules.append(line)
					elif '=' in line:
						self.facts = list(line.split('=')[1])
					elif '?' in line:
						self.queries = list(line.split('?')[1])
				print self.rules
				print self.facts
				print self.queries
		except IOError as err:
			print(err.strerror)

	def validRules(self, rules, i):
		prev = None
		count = 0
		op = ['+', '|', '^']
		par = ['(', ')']

		for j, char in enumerate(rules):
			if self.isUpperAlpha(char) and self.isUpperAlpha(prev):
				exitWithErrors("Wrong format at line " + str(i))
			elif not char in op and not char in par and not self.isUpperAlpha(char) and char != '!':
				exitWithErrors("Wrong format at line " + str(i))
			elif char == par[0]:
				count += 1
				if self.isUpperAlpha(prev):
					exitWithErrors("Wrong format at line " + str(i))
			elif char == par[1]:
				if count <= 0 or (not self.isUpperAlpha(prev) and prev != par[1]):
					exitWithErrors("Wrong format at line " + str(i))
				count -= 1
			elif char in op and ((not self.isUpperAlpha(prev) and not prev == par[1]) or j == len(rules)):
				exitWithErrors("Wrong format at line " + str(i))
			elif char == '!' and (self.isUpperAlpha(prev) or j == len(rules)):
				exitWithErrors("Wrong format at line " + str(i))

			prev = char

	def isUpperAlpha(self, char):
		return (not char is None) and char.isalpha() and char.isupper()
