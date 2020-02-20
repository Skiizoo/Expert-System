from token import Type, Token


def plus(tab, i):
	a = tab.pop(i - 2)
	b = tab.pop(i - 2)
	tab[i - 2] = a and b
	return -2


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


class Calc:

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

	def __init__(self, controller):
		self.controller = controller

	def calc(self, array):
		i = 0
		while len(array) > 1:
			token = Token(array[i])
			if token is Type.Operator:
				i += self.operators[array[i]]['calc'](array, i)
			i += 1
		return array


# op = ['+', '|', '^', '!']
#shutting = [False, False, '|', '!', True, '!', '+']
# index = 0
#
# while len(shutting) > 1:
# 	tok = shutting[index]
# 	if tok in op:
# 		index += operators[tok]['calc'](shutting, index)
# 	index += 1
# print(shutting)
