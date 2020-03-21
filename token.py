from enumerate import Type
from display import display_infos
from error import SolveError


class Token:
    __instances = {}

    def __init__(self, char):
        self.char = char

    def __new__(cls, value):
        type_token = Type.from_value(value)
        if type_token is not Type.Letter:
            instance = object.__new__(cls)
            instance.type = type_token
            if type_token is Type.Operator:
                instance.precedence = ['<=>', '=>', '^', '|', '+', '!'].index(value)
            return instance
        if value not in cls.__instances.keys():
            cls.__instances[value] = object.__new__(cls)
            cls.__instances[value].type = type_token
            cls.__instances[value].rules = [[None, None]]
            cls.__instances[value].__value = None
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
            display_infos("Token.py", "@property getter", "50", "Token " + self.char + " is False")
            return False
        elif len(self.rules) == 1:
            display_infos("Token.py", "@property getter", "50", "Token " + self.char + " is " + str(self.__value))
            return self.__value
        display_infos("Token.py", "@property getter", "50", "We don't know yet the value of Token " + self.char)
        return self.calc()

    @value.setter
    def value(self, new_value):
        if self.__value is not None and self.__value != new_value:
            raise SolveError("Token.py", "@property setter", "62", "Conflict value for Token " + self.char)
        self.__value = new_value
        display_infos("Token.py", "@property setter", "64", "Token " + self.char + " is now " + str(new_value))
        if len(self.rules) > 1:
            self.__value = self.calc()

    def calc_expression(self, str_expr):
        display_infos("Token.py", "calc_expression", "68", "Solving Token " + self.char + " of expression " + str_expr)
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
        display_infos("Token.py", "calc_conclusion", "77", "Solving Token " + self.char + " of conclusion " + str_ccl)
        # todo: or et xor
        if self == '+':
            self.right.calc_conclusion(str_ccl)
            self.left.calc_conclusion(str_ccl)
        elif self == '!':
            self.right.calc_conclusion(str_ccl, not value)
        else:
            self.value = value

    def calc(self):
        display_infos("Token.py", "calc", "89", "Looking for Token " + self.char + "'s value")
        token = self.rules.pop(0)
        if token[0] is not None:
            display_infos("Token.py", "calc", "91", "Looking into Token " + self.char + "'s rule: " + token[1])
            str_rule = token[1].split('=>')
        if token[0] is not None and token[0].left.calc_expression(str_rule[0]) is True:
            token[0].right.calc_conclusion(str_rule[1])
        elif self.value is True:
            token[0].right.calc_conclusion(str_rule[1])
        return self.value

    # def print(self):
    #     queue = [self]
    #     len_three = self.len()
    #     size = [len_three]
    #     tab = {1: 1, 2: 2, 3: 4, 4: 8, 5: 16, 6: 32}
    #     min_tab = [tab[len_three]]
    #     nb_tab = 0
    #     while len(queue):
    #         min_ta = min_tab[0]
    #         print(min_ta)
    #         height = size[0]
    #         token = queue[0]
    #         len_tab = tab[height]
    #         print('\t' * len_tab, end='')
    #         nb_tab += len_tab
    #         print(token.char, end='')
    #         print('\t' * len_tab, end='')
    #         nb_tab += len_tab
    #         queue.pop(0)
    #         size.pop(0)
    #         min_tab.pop(0)
    #         if token == '!':
    #             queue.append(token.right)
    #             size.append(height - 1)
    #             min_tab.append(min_ta - len_tab / 2)
    #         elif token.type is Type.Operator:
    #             queue.append(token.left)
    #             size.append(height - 1)
    #             min_tab.append(min_ta - len_tab / 2)
    #             queue.append(token.right)
    #             size.append(height - 1)
    #             min_tab.append(min_ta - len_tab / 2)
    #         else:
    #             pass
    #         if height not in size:
    #             nb_tab = 0
    #             print('')
    #
    # @staticmethod
    # def contains_len(queue, len) -> bool:
    #     for token in queue:
    #         if token.len() == len:
    #             return True
    #     return False
    #
    # def len(self):
    #     if self == '!':
    #         return 1 + self.right.len()
    #     elif self.type is Type.Operator:
    #         return 1 + max(self.right.len(), self.left.len())
    #     else:
    #         return 1
