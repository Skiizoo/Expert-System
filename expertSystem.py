from rule import Rule


class ExpertSystem:

	def __init__(self, rules, facts, queries):
		self.rules = map(Rule, rules)
		self.facts = []
		self.queries = []
		self.queries = []
		self.facts = []
		self.solve()

	def solve(self):
		for rule in self.rules:
			print(rule.expression)
		#todo
		return
