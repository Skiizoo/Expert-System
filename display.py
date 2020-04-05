from enumerate import Type

debug = None
tree = None


class Bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BOLDnBLUE = '\033[1m\033[94m'
    BOLDnGREEN = '\033[1m\033[92m'
    BOLDnRED = '\033[1m\033[91m'
    UNDnRED = '\033[4m\033[91m'


def display_result(char, value):
    print(f'{Bcolors.BOLDnGREEN} Result: {Bcolors.END} {char} is {value}')


def display_infos(file, func, line, txt):
    if debug is True:
        print(('{BOLDnBLUE} File: {END} {BLUE} {FILE:18} {END}'
               '{BOLDnBLUE} Function {END} {BLUE} {FUNC:18} {END}'
               '{BOLDnBLUE} Line: {END} {BLUE} {LINE:4} {END} {TXT}').format(
            BOLDnBLUE=Bcolors.BOLDnBLUE, END=Bcolors.END, BLUE=Bcolors.BLUE, FILE=file, FUNC=func, LINE=line, TXT=txt))


def display_parse_error(file, line, i, txt, j):
    if j is not None:
        line = '{FAIL}{S_LINE}{END}{BOLDnRED}{I_CHAR}{END}{FAIL}{E_LINE}{END}'.format(
            END=Bcolors.END, BOLDnRED=Bcolors.UNDnRED, FAIL=Bcolors.FAIL, S_LINE=line[:j - 1], I_CHAR=line[j - 1],
            E_LINE=line[j:])
    return ('{BOLDnRED} {TYPE:26} {END}'
            '{BOLDnRED} File: {END} {FAIL} {FILE:21} {END}'
            '{BOLDnRED} Line: {END} {FAIL} {I:2} {END} {FAIL}  {LINE} {END} {TXT} ').format(
        BOLDnRED=Bcolors.BOLDnRED, END=Bcolors.END, FAIL=Bcolors.FAIL, TYPE="PARSING ERROR", FILE=file, I=i, LINE=line,
        TXT=txt)


def display_solve_error(file, func, line, txt):
    return ('{BOLDnRED} {TYPE:26} {END}'
            '{BOLDnRED} File: {END} {FAIL} {FILE:21} {END}'
            '{BOLDnRED} Function: {END} {FAIL} {FUNC:21} {END}'
            '{BOLDnRED} Line: {END} {FAIL} {LINE:2} {END} {TXT} ').format(
        BOLDnRED=Bcolors.BOLDnRED, END=Bcolors.END, FAIL=Bcolors.FAIL, TYPE="SOLVING ERROR", FILE=file, FUNC=func,
        LINE=line, TXT=txt)


def display_file_error(file):
    return '{BOLDnRED} No such file: {END} {FAIL} \'  \' {END}'.format(
        BOLDnRED=Bcolors.BOLDnRED, END=Bcolors.END, FAIL=Bcolors.FAIL, TYPE="SOLVING ERROR", FILE=file)


def display_tree(char, rules, tab=[], depth=0, token=None, init=False):
    if tree is True:
        if token is not None:
            if depth > len(tab):
                tab.append([])
            if token.type is Type.Operator:
                if token.char != "!":
                    display_tree(char, rules, tab, depth + 1, token.left, True)
                tab[depth - 1].append([token.char, my_max(tab) + 1])
                display_tree(char, rules, tab, depth + 1, token.right, True)
                if depth == 1 and len(rules) > 1:
                    display_tree(char, rules, tab, 1, rules.pop(0)[0], True)
            elif token.type is Type.Letter:
                tab[depth - 1].append([token.char, my_max(tab) + 1])
        elif depth == 0 and len(rules) > 1:
            display_tree(char, rules, tab, 1, rules.pop(0)[0], True)
        if init is False and len(tab) > 0:
            print('{BOLDnBLUE} Representation of {TOKEN}\'s trees {END}'.format(
                BOLDnBLUE=Bcolors.BOLDnBLUE, END=Bcolors.END, TOKEN=char))
            print('\n'.join([''.join(['{BLUE}{TOKEN:>{POS}}{END}'.format(BLUE=Bcolors.BLUE, END=Bcolors.END,
                                                                         TOKEN=item[0],
                                                                         POS=item[1] * 3 - row[w - 1][1] * 3
                                                                         if w > 0 else item[1] * 3) for w, item in
                                      enumerate(row)]) for row in tab]))


def my_max(tab):
    maximum = 0
    if not tab:
        return maximum
    for t in tab:
        for j in t:
            if maximum < j[1]:
                maximum = j[1]
    return maximum
