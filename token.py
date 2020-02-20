from lovni import Type


def minus(tab, i):
	a = tab.pop(i - 2)
	b = tab.pop(i - 2)
	tab[i - 2] = a or b
	return -2


def xor(tab, i):
	a = tab.pop(i - 2)
	b = tab.pop(i - 2)
	tab[i - 2] = (a or b) and not (a and b)
	return -2


def negation(tab, i):
	a = tab.pop(i - 1)
	tab[i - 1] = not a
	return -1


def plus(tab, i):
	a = tab.pop(i - 2)
	b = tab.pop(i - 2)
	tab[i - 2] = a and b
	return -2


class Token:

	operators = {
		'+': {
			'prec': 1,
			'assoc': 'left',
			'calc': lambda tab, i: plus(tab, i)
		}, '|': {
			'prec': 2,
			'assoc': 'left',
			'calc': lambda tab, i: minus(tab, i)
		}, '^': {
			'prec': 3,
			'assoc': 'left',
			'calc': lambda tab, i: xor(tab, i)
		}, '!': {
			'prec': 6,
			'assoc': 'right',
			'arity': 1,
			'calc': lambda tab, i: negation(tab, i)
		}
	}

	def __init__(self, char):
		self.type = Type.from_char(char)
		self.value = char

	def getvalue(self, array, index):
		return self.operators[self.value]['calc'](array, index)

	def __gt__(self, other):
		return self.operators.index(self.value) > other.operators.index(other.value)
