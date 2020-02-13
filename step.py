from enum import Enum


class Step(Enum):
	rules = 0
	facts = 1
	queries = 2

	def __next__(self):
		return None if self is Step.queries else Step(self.value + 1)
