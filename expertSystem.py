from rule import Rule

#from typing import Optional
#Value = Optional[bool]

class ExpertSystem:

	def __init__(self, rules, facts, queries):
		self.rules = map(Rule, rules)
		self.facts = []
		self.queries = []
		# self.queries = [Value]
		# self.facts = [Optional[bool]] # initialize facts
		self.solve()

	def solve(self):
		for rule in self.rules:
			print rule.expression
		#todo
		return
