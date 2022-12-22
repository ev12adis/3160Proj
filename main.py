#Evan Adis 3160 Project

from sly import Lexer
from sly import Parser


# GRAMMAR

@_('')
def statement(self, x):
    pass


@_('var_assign')
def statement(self, x):
    return x.var_assign


@_('LETTER"=" expr')
def var_assign(self, x):
    return ('var_assign', x.LETTER, x.expr)


@_('LETTER"=" STRING')
def var_assign(self, x):
    return('var_assign', x.LETTER, x.STRING)


@_('expr')
def statement(self, x):
    return(x.expr)


@_('expr"=" expr')
def expr(self, x):
    return ('add', x.expr0, x.expr1)


@_('expr"-" expr')
def expr(self, x):
    Return('mul', x.expr0, x.expr1)


@_('expr"/" expr')
def expr(self, x):
    return ('div', x.expr0, x.expr1)


@_('"-" expr%prec UMINUS')
def expr(self, x):
    return x.expr


@_('LETTER')
def expr(self, x):
    return ('var', x.LETTER)


@_('DIGIT')
def expr(self, x):
    return('num', x.DIGIT)



class myLex(Lexer):
    tokens = {LETTER, DIGIT, STRING}
    ignore = '\t'

    literals = {'=', '+', '-', '/', '*', ',', ';', '(', ')'}

    # defines tokens for strings
    STRING = r'\".*?\"'
    # defines tokens of letters
    LETTER = r'[a-zA-Z0-9_][a-zA-Z_]*'

    @_(r'0|[0-9][1-9]*')
    def DIGIT(self, x):
        x.value = int(x.value)
        return x


# PARSER CLASS
class myParser(Parser):
    tokens = myLex.tokens
    # retrieves from myLex class

    __ORDER_BIG_ENDIAN__ = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
    )

    def __init__(self):
        self.env = {}


# /recursive tree


class run:
    def__init__(self, tree, env):
        self.env = env
        result = self.parseTree(tree)
        if result is not None and isinstance(result, int):
            print(result)

    def parseTree(self, node):
        if isinstance(node, int):
            return node
        if isinstance(node, str):
            return node
        if node is None:
            return None
        if node[0] == 'program':
            if node[1] == None:
                self.parseTree(node[2])
            else:
                self.parseTree(node[1])
                self.parseTree(node[2])
        if node[0] == 'num':
            return node[1]
        if node[0] == 'str':
            return node[1]
        if node[0] == 'condition_eqeq':
            return self.parseTree(node[1]) == self.parseTree(node[2])
        if node[0] == 'add':
            return self.parseTree(node[1]) + self.walktree(node[2])
        elif node[0] == 'sub':
            return self.parseTree(node[1]) - self.parseTree(node[2])
        elif node[0] == 'mul':
            return self.parseTree(node[1]) * self.parseTree(node[2])
        elif node[0] == 'div':
            return self.parseTree(node[1]) / self.parseTree(node[2])
        if node[0] == 'var_assign':
            self.env[node[1]] = self.parseTree(node[2])
            return node[1]
        if node[0] == 'var':
            try:
                return self.env[node[1]]
            except LookupError:
                print(" variable - undefined '"+node[1]+"'.")
                return 0


if __name__ =='__main__':
    lexer = myLex()
    parser = myParser()
    env = {}
    while True:
        try:
            text = input('Enter expression:')
        except EOFError:
            break
        if text:
            tree = parser.parse(lexer, tokenize(text))
            run(tree, env)
