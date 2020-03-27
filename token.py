from enumerate import Type
from display import display_infos, display_tree, display_treeV2
from error import SolveError


def my_max(tab):
    maximum = 0
    if not tab:
        return maximum
    for t in tab:
        for j in t:
            if maximum < j[1]:
                maximum = j[1]
    return maximum


class Token:
    __instances = {}

    def __init__(self, char):
        self.char = char

    def __new__(cls, value):
        type_token = Type.from_value(value)
        if type_token is not Type.Letter:
            display_infos("Token.py", "__new__", "15", "Creation of specific Token operator " + value)
            instance = object.__new__(cls)
            instance.type = type_token
            if type_token is Type.Operator:
                instance.precedence = ['<=>', '=>', '^', '|', '+', '!'].index(value)
            return instance
        if value not in cls.__instances.keys():
            display_infos("Token.py", "__new__", "22", "Creation of global Token operator " + value)
            cls.__instances[value] = object.__new__(cls)
            cls.__instances[value].type = type_token
            cls.__instances[value].rules = [[None, None]]
            cls.__instances[value].__value = None
        else:
            display_infos("Token.py", "__new__", "28", "Global Token operator " + value + " already exists")
        return cls.__instances[value]

    def __gt__(self, other):
        return self.precedence > other.precedence

    def __lt__(self, other):
        return self.precedence < other.precedence

    def __le__(self, other):
        return self.precedence <= other.precedence

    def __ge__(self, other):
        return self.precedence >= other.precedence

    def __str__(self):
        return self.char

    def __repr__(self):
        return self.char

    def __eq__(self, other):
        return self.char == other

    @property
    def value(self):
        if len(self.rules) == 1 and self.__value is None:
            display_infos("Token.py", "@property getter", "55", "Token " + self.char + " is False")
            return False
        elif len(self.rules) == 1:
            display_infos("Token.py", "@property getter", "58", "Token " + self.char + " is " + str(self.__value))
            return self.__value
        display_infos("Token.py", "@property getter", "60", "We don't know yet the value of Token " + self.char)
        return self.calc()

    @value.setter
    def value(self, new_value):
        if self.__value is not None and self.__value != new_value:
            raise SolveError("Token.py", "@property setter", "66", "Conflict value for Token " + self.char)
        self.__value = new_value
        display_infos("Token.py", "@property setter", "68", "Token " + self.char + " is now " + str(new_value))
        if len(self.rules) > 1:
            self.__value = self.calc()

    def calc_expression(self, str_expr):
        display_infos("Token.py", "calc_expression", "73", "Solving Token " + self.char + " of expression " + str_expr)
        if self == '!':
            return not self.right.calc_expression(str_expr)
        elif self == '|':
            return self.left.calc_expression(str_expr) or self.right.calc_expression(str_expr)
        elif self == '+':
            return self.left.calc_expression(str_expr) and self.right.calc_expression(str_expr)
        elif self == '^':
            return self.left.calc_expression(str_expr) is not self.right.calc_expression(str_expr)
        else:
            return self.value

    def calc_conclusion(self, str_ccl, value=True):
        display_infos("Token.py", "calc_conclusion", "86", "Solving Token " + self.char + " of conclusion " + str_ccl)
        # todo: or et xor
        if self == '+':
            self.right.calc_conclusion(str_ccl)
            self.left.calc_conclusion(str_ccl)
        elif self == '!':
            self.right.calc_conclusion(str_ccl, not value)
        else:
            self.value = value

    def calc(self):
        display_infos("Token.py", "calc", "97", "Looking for Token " + self.char + "'s value")
        token = self.rules.pop(0)
        if token[0] is not None:
            display_infos("Token.py", "calc", "100", "Looking into Token " + self.char + "'s rule: " + token[1])
            str_rule = token[1].split('=>')
        if token[0] is not None and token[0].left.calc_expression(str_rule[0]) is True:
            token[0].right.calc_conclusion(str_rule[1])
        elif self.value is True:
            token[0].right.calc_conclusion(str_rule[1])
        return self.value

    def display(self, rules, depth, token="", tab=[], init=False):
        if token is not None:
            if depth > len(tab):
                tab.append([])
            if depth == 0 and len(rules) > 1:
                self.display(rules, 1, rules.pop(0)[0], tab, True)
            elif token.type is Type.Operator:
                self.display(rules, depth + 1, token.right, tab, True)
                # display_tree(token.char, depth)
                tab[depth - 1].append([token.char, my_max(tab) + 1])
                self.display(rules, depth + 1, token.left, tab, True)
                if depth == 1 and len(rules) > 1:
                    self.display(rules, 1, rules.pop(0)[0], tab, True)
            elif token.type is Type.Letter:
                # display_tree(token.char, depth)
                tab[depth - 1].append([token.char, my_max(tab) + 1])
        # todo correct multiple print
        if init is False:
            display_treeV2(tab)
