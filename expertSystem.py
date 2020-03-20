from rule import Rule
from token import Token


class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


class ExpertSystem:

	def __init__(self, parser):
		print(parser.rules)
		for rule in parser.rules:
			Rule(rule)
		print('Rule Done')
		for fact in parser.facts:
			Token(fact).value = True
		print('Fact Done')
		for query in parser.queries:
			Token(query).value
			print(bcolors.OKGREEN, '#', Token(query), 'is', Token(query).value, bcolors.ENDC)

