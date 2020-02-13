from enum import Enum


class Step(Enum):
	expr = 0
	facts = 1
	queries = 2

	def __next__(self):
		if self is Step.queries:
			return None
		return Step(self.value + 1)
