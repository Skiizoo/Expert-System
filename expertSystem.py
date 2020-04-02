from rule import Rule
from display import display_result, display_infos
from token import Token


class ExpertSystem:

	def __init__(self, parser):
		display_infos("ExpertSystem.py", "__init__", "9", "ExpertSystem Initialization")
		display_infos("Rule.py", "__init__", "10", "Starting creation of global graph")
		for rule in parser.rules:
			Rule(rule)
		display_infos("Rule.py", "__init__", "13", "Assigning Facts value at True")
		for fact in parser.facts:
			Token(fact).value = True
		for query in parser.queries:
			display_infos("ExpertSystem.py", "__init__", "17", "Solve and deduct of " + query + "'s query")
			rules = Token(query).rules
			Token(query).display(rules, 0)
			value = Token(query).value
			value = value if value is not None else False
			display_result(query, value)
