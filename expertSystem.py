from rule import Rule
from display import display_result, display_infos
from token import Token
from enumerate import Value


class ExpertSystem:

	def __init__(self, parser):
		display_infos("ExpertSystem.py", "__init__", "10", "ExpertSystem Initialization")
		display_infos("ExpertSystem.py", "__init__", "11", "Starting creation of global graph")
		for rule in parser.rules:
			Rule(rule)
		for query in parser.queries:
			rules = Token(query).rules[:]
			Token(query).display(rules, [])
		display_infos("ExpertSystem.py", "__init__", "17", "Assigning Facts value at True")
		for fact in parser.facts:
			Token(fact).value = Value.true
		for query in parser.queries:
			display_infos("ExpertSystem.py", "__init__", "21", "Solve and deduct of " + query + "'s query")
			display_result(query, Token(query).value)
