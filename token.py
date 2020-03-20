from enumerate import Type


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
            cls.__instances[value].rules = [None]
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
        #print('getter', self, self.__value)
        if len(self.rules) == 1 and self.__value is None:
            return False
        elif len(self.rules) == 1:
            return self.__value
        return self.calc()

    @value.setter
    def value(self, new_value):
        print('setter start', self, self.__value, new_value)
        if self.__value is not None and self.__value != new_value:
            print('lksfk;skdf;sf')
            #todo: gestion erreur + debug
            exit(self)
        self.__value = new_value
        if len(self.rules) > 1:
            self.__value = self.calc()
        #print('setter end', self, self.__value)

    def calc_expression(self):
        #print('calc_expression', self)
        if self == '!':
            return not self.right.calc_expression()
        elif self == '|':
            return self.left.calc_expression() or self.right.calc_expression()
        elif self == '+':
            return self.left.calc_expression() and self.right.calc_expression()
        elif self == '^':
            return self.left.calc_expression() is not self.right.calc_expression()
        else:
            return self.value

    def calc_conclusion(self, value=True):
        # todo: or et xor
        print('calc_conclu', self)
        if self == '+':
            self.right.calc_conclusion()
            self.left.calc_conclusion()
        elif self == '!':
            self.right.calc_conclusion(value=False)
        else:
            self.value = value

    def calc(self):
        print('calc', self)
        token = self.rules.pop(0)
        if token is not None and token.left.calc_expression() is True:
            token.right.calc_conclusion()
        elif self.value is True:
            token.right.calc_conclusion()
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
