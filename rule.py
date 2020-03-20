from token import Token
from enumerate import Type
import re


class Rule:

    def __init__(self, rule):
        self.rule = list(map(Token, rule))
        ccl = ''.join(rule).split('=>')[1]
        ccl_letters = re.findall(r'[A-Z]', ccl)
        impl_token = list(filter(lambda x: x == '=>', self.rule))[0]
        for letter in ccl_letters:
            Token(letter).rules.insert(0, impl_token)
        self.output = []
        self.shunting_yard()
        #impl_token.print()
        #exit()

    def __str__(self):
        return self.output

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
