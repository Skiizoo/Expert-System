from enum import Enum


class Type(Enum):
	Operator = 1
	Letter = 2

	@classmethod
	def from_char(cls, char):
		if char.isalpha() and char.isupper():
			return cls.Letter
		return cls.Operator


class Token:

	def __init__(self, char):
		self.type = Type.from_char(char)
