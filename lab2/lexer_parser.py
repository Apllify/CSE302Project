#! /usr/bin/env python3

# --------------------------------------------------------------------
# Requires Python3 >= 3.10

# --------------------------------------------------------------------
import abc
import argparse
import bisect
import dataclasses as dc
import json
import os
import ply.lex
import ply.yacc
import re
import sys
import typing as tp

import ASTHelper as ast
# ====================================================================
# Parse tree / Abstract Syntax Tree

# --------------------------------------------------------------------
@dc.dataclass
class Name:
    value: str

# --------------------------------------------------------------------
class Expression:
    pass

# --------------------------------------------------------------------
@dc.dataclass
class VarExpression(Expression):
    name: Name

# --------------------------------------------------------------------
@dc.dataclass
class IntExpression(Expression):
    value: int

# --------------------------------------------------------------------
@dc.dataclass
class OpAppExpression(Expression):
    operator: str
    arguments: list[Expression]

# --------------------------------------------------------------------
class Statement:
    pass

# --------------------------------------------------------------------
@dc.dataclass
class VarDeclStatement(Statement):
    name: Name
    init: Expression

# --------------------------------------------------------------------
@dc.dataclass
class AssignStatement(Statement):
    lhs: Name
    rhs: Expression

# --------------------------------------------------------------------
@dc.dataclass
class PrintStatement(Statement):
    value: Expression

# --------------------------------------------------------------------
Program = list[Statement]

# ====================================================================
# BX lexer definition

class Lexer:
    # FIXME: complete the lexer
    # DONE: - add all tokens
    # DONE: - add all lexing entries (t_XXX)

    reserved = {
        "print" : "PRINT",
        "while" : "WHILE",
        "int" : "INT",
        "var" : "VAR",
        "def" : "DEF"
    }

    tokens = (                  # FIXME (add more tokens)
        'IDENT' ,
        'NUMBER',

        'PLUS'  ,
        "MINUS",
        "PRODUCT",
        "DIVISION",
        "MODULO",

        "AND",
        "OR",
        "XOR",
        "LSHIFT",
        "RSHIFT",
        "INVERSE",

        "EQUAL",


        "COLON",
        "SEMICOLON",


        "LPAREN",
        "RPAREN",
        "LCURLYBRACKET",
        "RCURLYBRACKET"

    ) + tuple(reserved.values())

    #characters to skip 
    t_ignore = re.escape(" \t\f\v")

    #regex expressions for all of the tokens that don't need a payload
    t_PLUS = re.escape('+') 
    t_MINUS = re.escape("-")
    t_PRODUCT = re.escape("*")
    t_DIVISION = re.escape("/")
    t_MODULO = re.escape("%")

    t_AND = re.escape("&")
    t_OR = re.escape("|")
    t_XOR = re.escape("^")
    t_LSHIFT = re.escape("<<")
    t_RSHIFT = re.escape(">>")
    t_INVERSE = re.escape("~")

    t_EQUAL = re.escape("=")

    t_COLON = re.escape(":")
    t_SEMICOLON = re.escape(";")

    t_LPAREN = re.escape("(")
    t_RPAREN = re.escape(")")
    t_LCURLYBRACKET = re.escape("{")
    t_RCURLYBRACKET = re.escape("}")



    def __init__(self):
        self.nerrors = 0
        self.linenumber = 1

    # Regular expression + processing for tokens with a semantic value
    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_IDENT(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'

        if t in Lexer.reserved.keys():
            t.type = Lexer.reserved[t]

        return t

    def t_error(self, t):
        print(f"illegal character: `{t.value[0]}' in line : {self.linenumber}", file = sys.stderr)
        self.nerrors += 1
        t.lexer.skip(1) 

    def t_newline(self, t):
        r'\n'
        self.linenumber += 1
    


    @classmethod
    def build(cls, **kw):
        instance = cls()
        # instance.lexer = ply.lex.lex(instance, **kw)
        instance.lexer = ply.lex.lex(module = instance, **kw)
        return instance






# ====================================================================
# BX parser definition

class Parser:
    UNIOP = {
        '-' : 'opposite'        ,
        '~' : 'bitwise-negation',
    }

    BINOP = {
        '+'  : 'addition'           ,
        '-'  : 'subtraction'        ,
        '*'  : 'multiplication'     ,
        '/'  : 'division'           ,
        '%'  : 'modulus'            ,
        '>>' : 'logical-right-shift',
        '<<' : 'logical-left-shift' ,
        '&'  : 'bitwise-and'        ,
        '|'  : 'bitwise-or'         ,
        '^'  : 'bitwise-xor'        ,
    }

    tokens = Lexer.tokens
    
    start = 'prgm'

    precedence = ()             # FIXME: set the correct precedence

    def p_name(self, p):
        """name : IDENT"""
        p[0] = Name(value = p[1])

    def p_expression_int(self, p):
        """expr : NUMBER"""
        p[0] = IntExpression(value = p[1])

    def p_expression_add(self, p):
        """expr : expr PLUS  expr"""

        p[0] = OpAppExpression(
            operator  = self.BINOP[p[2]],
            arguments = [p[1], p[3]],
        )

    def p_prgm(self, p):
        """prgm : """           # FIXME: fix the parser
        p[0] = None

    def p_error(self, p):
        self.lexer.nerrors += 1

        if p:
            print(f'syntax error at token {p.value}', file = sys.stderr)
            self.parser.errok()
        else:
            print('syntax error at EOF', file = sys.stderr)

    @classmethod
    def build(cls):
        instance = cls()
        instance.parser = ply.yacc.yacc(module = instance)
        instance.lexer  = Lexer.build()
        return instance

    @classmethod
    def parse(cls, program : str):
        instance = cls.build()

        ast = instance.parser.parse(
            program,
            lexer    = instance.lexer.lexer,
            tracking = True,
        )

        return ast if instance.lexer.nerrors == 0 else None

# ====================================================================
# Syntax-level checker

class SynChecker:
    def __init__(self):
        pass

    def for_program(self, prgm : Program):
        # FIXME: check that `prgm` is syntactical correct
        pass

    @classmethod
    def check(cls, prgm : Program):
        checker = cls()
        checker.for_program(prgm)
        return (checker.nerrors == 0)

# ====================================================================
# Three-Address Code

OPCODES = {
    'opposite'            : 'neg',
    'addition'            : 'add',
    'subtraction'         : 'sub',
    'multiplication'      : 'mul',
    'division'            : 'div',
    'modulus'             : 'mod',
    'bitwise-negation'    : 'not',
    'bitwise-and'         : 'and',
    'bitwise-or'          :  'or',
    'bitwise-xor'         : 'xor',
    'logical-shift-left'  : 'shl',
    'logical-shift-right' : 'shr',
}

# --------------------------------------------------------------------
@dc.dataclass
class TAC:
    opcode    : str
    arguments : list[str]
    result    : tp.Optional[str] = None

    def tojson(self):
        return dict(
            opcode = self.opcode   ,
            args   = self.arguments,
            result = self.result   ,
        )

# ====================================================================
# Maximal munch

class MM:
    def __init__(self):
        self._counter = -1
        self._tac     = []
        self._vars    = {}

    tac = property(lambda self : self._tac)

    @staticmethod
    def mm(prgm : Program):
        mm = MM(); mm.for_program(prgm)
        return mm._tac

    def fresh_temporary(self):
        self._counter += 1
        return f'%{self._counter}'

    def push(
            self,
            opcode     : str,
            *arguments : str,
            result     : tp.Optional[str] = None,
    ):
        self._tac.append(TAC(opcode, list(arguments), result))

    def for_program(self, prgm : Program):
        for stmt in prgm:
            self.for_statement(stmt)

    def for_statement(self, stmt : Statement):
        match stmt:
            case VarDeclStatement(name):
                self._vars[name.value] = self.fresh_temporary()
                self.push('const', '0', self._vars[name.value])

            case AssignStatement(lhs, rhs):
                temp = self.for_expression(rhs)
                self.push('copy', temp, result = self._vars[lhs.value])

            case PrintStatement(value):
                temp = self.for_expression(value)
                self.push('print', temp)

    def for_expression(self, expr : Expression) -> str:
        target = None

        match expr:
            case VarExpression(name):
                target = self._vars[name.value]

            case IntExpression(value):
                target = self.fresh_temporary()
                self.push('const', str(value), result = target)

            case OpAppExpression(operator, arguments):
                target    = self.fresh_temporary()
                arguments = [self.for_expression(e) for e in arguments]
                self.push(OPCODES[operator], *arguments, result = target)

        return target

# ====================================================================
# Parse command line arguments

def parse_args():
    parser = argparse.ArgumentParser(prog = os.path.basename(sys.argv[0]))

    parser.add_argument('input' , help = 'input file (.bx)')
    parser.add_argument('output', help = 'output file (.tac.json)')

    return parser.parse_args()

# ====================================================================
# Main entry point

def _main():
    args = parse_args()

    try:
        with open(args.input, 'r') as stream:
            prgm = stream.read()

    except IOError as e:
        print(f'cannot read input file {args.input}: {e}')
        exit(1)    


    prgm = Parser.parse(prgm)

    if prgm is None:
        exit(1)

    print(prgm)

    if not SynChecker.check(prgm):
        exit(1)

    tac = MM.mm(prgm)

    aout = [dict(
        proc = '@main',
        body = [x.tojson() for x in tac],
    )]

    try:
        with open(args.output, 'w') as stream:
            json.dump(aout, stream, indent = 2)
            print(file = stream) # Add a new-line

    except IOError as e:
        print(f'cannot write outpout file {args.output}: {e}')
        exit(1)

# --------------------------------------------------------------------
if __name__ == '__main__':
    _main()
