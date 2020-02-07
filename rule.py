class Rule:

	def __init__(self, rule):
		self.expression = rule.split('=>')[0]
		self.conclusion = rule.split('=>')[1]
		self.save = rule
		self.dict = []