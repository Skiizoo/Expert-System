from enum import Enum

class Type(Enum):
    Letter = 0
    Operator = 1
    LeftParen = 2
    RightParen = 3

    @classmethod
    def from_value(cls, value):
        if value == '(':
            return cls.LeftParen
        elif value == ')':
            return cls.RightParen
        elif value.isupper():
            return cls.Letter
        else:
            return cls.Operator


class Token:
    __instances = {}

    def __init__(self, char):
        self.char = char
        self.__value = False
        if self.type is Type.Operator:
            self.precedence = ['<=>', '=>', '^', '|', '+', '!'].index(char)

    def __new__(cls, value):
        type_token = Type.from_value(value)
        if type_token is not Type.Letter:
            instance = object.__new__(cls)
            instance.type = type_token
            return instance
        if value not in cls.__instances.keys():
            cls.__instances[value] = object.__new__(cls)
            cls.__instances[value].type = type_token
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
        if self.__value:
            return

    @value.setter
    def value(self, instance, new_value):
        if self.__value:
            pass
        else:
            self.__value = new_value


class Rule:

    def __init__(self, rule: str):
        self.fact = ['C']
        self.rule = map(Token, rule)
        self.output = []
        self.shunting_yard()
        print(self.output)
        print(self.calc(self.output[0]))

    def shunting_yard(self):
        operator = []
        for token in self.rule:
            if token.type is Type.Letter:
                self.output.append(token)
            if token.type is Type.Operator:
                while len(operator) and operator[-1].type is not Type.LeftParen and (operator[-1] > token):
                    self.push_operator_to_output(operator.pop())
                operator.append(token)
            if token.type is Type.LeftParen:
                operator.append(token)
            if token.type is Type.RightParen:
                while len(operator) and operator[-1].type is not Type.LeftParen:
                    self.push_operator_to_output(operator.pop())
                operator.pop()
        while len(operator):
            self.push_operator_to_output(operator.pop())

    def push_operator_to_output(self, token: Token):
        if token == '!':
            token.right = self.output.pop()
        else:
            token.right = self.output.pop()
            token.left = self.output.pop()
        self.output.append(token)

    def calc_expression(self, token):
        print(token)
        if token == '!':
            return not self.calc_expression(token.right)
        elif token == '|':
            return self.calc(token.left) | self.calc(token.right)
        elif token == '+':
            return self.calc(token.left) & self.calc(token.right)
        else:
            return token.

    def calc_conclusion(self, token):
        pass

    def calc(self, token):
        result = token.left
        if result == True:
            pass
        else:
            return None

Rule(['A','|','(','B','+','C',')','=>','D', '+', 'E'])
