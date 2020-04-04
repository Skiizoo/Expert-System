import re
from error import ParseError
from enumerate import Step
from display import display_infos

#todo: double implication
class Parse:

    def __init__(self, controller):
        display_infos("Parse.py", "__init__", "10", "Parsing Initialization")
        self.controller = controller
        self.rules = []
        self.facts = []
        self.queries = []
        self.get_params()

    def get_params(self):
        display_infos("Parse.py", "get_params", "18", "Opening the " + self.controller.pathToFile + " file")
        with open(self.controller.pathToFile) as f:
            current_step = Step.rules
            file = [x for x in re.sub(r'(#.*)|([\t ])', '', f.read()).split('\n') if x]

            for i, line in enumerate(file):
                if current_step is None:
                    raise ParseError(self.controller.pathToFile, line, i, "Multiple lines of queries found, should be "
                                                                          "all in one")
                if current_step is Step.rules:
                    if self.valid_rule(line, i):
                        rule = re.findall(r'=>|.', line)

                        self.rules.append(rule)
                        display_infos("Parse.py", "get_params", "31", "Rule: {}".format(rule))
                    else:
                        current_step = next(current_step)
                if current_step is Step.facts:
                    if not self.valid_fact(line, i):
                        raise ParseError(self.controller.pathToFile, line, i, "Facts isn't well computed. Must be "
                                                                              "like r'^=(?!.*?(.).*?\\1)[A-Z]*$'")
                    self.facts = re.sub(r'=', '', line)
                    display_infos("Parse.py", "get_params", "39", "Facts: " + self.facts)
                    current_step = next(current_step)
                elif current_step is Step.queries:
                    if not self.valid_query(line, i):
                        raise ParseError(self.controller.pathToFile, line, i, "Queries isn't well computed. Must be "
                                                                              "like r'^\\?(?!.*?(.).*?\\1)[A-Z]*$'")
                    self.queries = re.sub(r'\?', '', line)
                    display_infos("Parse.py", "get_params", "46", "Queries: " + self.queries)
                    current_step = next(current_step)

    def valid_rule(self, line, i) -> bool:
        op = ['+', '|', '^']
        par = ['(', ')']
        ind_error = -2

        if self.valid_fact(line, i) or line[0] == '=':
            return False
        if self.valid_query(line, i):
            raise ParseError(self.controller.pathToFile, line, i, "Facts missing")
        rules = line.split('=>')
        if len(rules) != 2:
            raise ParseError(self.controller.pathToFile, line, i, "Rules isn't well computed")
        for rule in rules:
            ind_error += 2
            prev = None
            count = 0
            for j, char in enumerate(rule):
                ind_error += 1
                if self.is_upper_alpha(char) and self.is_upper_alpha(prev):
                    raise ParseError(self.controller.pathToFile, line, i, "Two characters A-Z are following", ind_error)
                elif char not in op and char not in par and not self.is_upper_alpha(char) and char != "!":
                    raise ParseError(self.controller.pathToFile, line, i, "Unknown character", ind_error)
                elif char == par[0]:
                    count += 1
                    if self.is_upper_alpha(prev):
                        raise ParseError(self.controller.pathToFile, line, i, "No operator before '('", ind_error)
                elif char == par[1]:
                    if count <= 0 or (not self.is_upper_alpha(prev) and prev != par[1]):
                        raise ParseError(self.controller.pathToFile, line, i, "Closed parenthesis not open", ind_error)
                    count -= 1
                elif char in op and ((not self.is_upper_alpha(prev) and not prev == par[1]) or j == len(line)):
                    raise ParseError(self.controller.pathToFile, line, i, "Incorrect character before operator",
                                     ind_error)
                elif char == '!' and (self.is_upper_alpha(prev) or j == len(rule)):
                    raise ParseError(self.controller.pathToFile, line, i, "Incorrect character after negation",
                                     ind_error)
                prev = char
        return True

    @staticmethod
    def valid_fact(line, i) -> bool:
        if re.match(r'^=(?!.*?(.).*?\1)[A-Z]*$', line):
            return True
        return False

    @staticmethod
    def valid_query(line, i) -> bool:
        if re.match(r'^\?(?!.*?(.).*?\1)[A-Z]*$', line):
            return True
        return False

    @staticmethod
    def is_upper_alpha(char):
        return char is not None and char.isalpha() and char.isupper()
