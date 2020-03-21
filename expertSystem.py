from rule import Rule
from display import display_result, display_infos
from token import Token


class ExpertSystem:

	def __init__(self, parser):
		display_infos("ExpertSystem.py", "__init__", "9", "ExpertSystem Initialization")
		for rule in parser.rules:
			Rule(rule)
		for fact in parser.facts:
			Token(fact).value = True
		for query in parser.queries:
			display_infos("ExpertSystem.py", "__init__", "15", "Solve and deduct of " + query + "'s query")
			value = Token(query).value
			display_result(query, value)
