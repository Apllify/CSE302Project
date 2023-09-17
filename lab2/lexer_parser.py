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
        "def" : "DEF",
        "main" : "MAIN"
    }

    tokens = (                 
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
        "COMPLEMENT",

        "EQUAL",


        "COLON",
        "SEMICOLON",


        "LPAREN",
        "RPAREN",
        "LCURLYBRACKET",
        "RCURLYBRACKET"

    ) + tuple(reserved.values())

    #characters to skip 
    t_ignore = " \t\f\v"


    # Regexp strings definitions beginning with ‘t_’ define simple tokens    
    t_PLUS = re.escape('+') 
    t_MINUS = "-"
    t_PRODUCT = re.escape("*")
    t_DIVISION = re.escape("/")
    t_MODULO = re.escape("%")

    t_AND = re.escape("&")
    t_OR = re.escape("|")
    t_XOR = re.escape("^")
    t_LSHIFT = re.escape("<<")
    t_RSHIFT = re.escape(">>")
    t_COMPLEMENT = re.escape("~")

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

        t.type = Lexer.reserved.get(t.value, "IDENT")

        return t

    def t_newline(self, t):
        r'\n'
        self.linenumber += 1

    def t_error(self, t):
        print(f"illegal character: `{t.value[0]}' in line : {self.linenumber}", file = sys.stderr)
        self.nerrors += 1
        t.lexer.skip(1) 


    


    @classmethod
    def build(cls, **kw):
        instance = cls()
        instance.lexer = ply.lex.lex(object = instance, **kw)
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

    precedence = (
        ("left", "OR"),
        ("left", "XOR"),
        ("left", "AND"),
        ("left", "LSHIFT", "RSHIFT"),
        ("left",   "PLUS", "MINUS"),
        ("left", "PRODUCT", "DIVISION", "MODULO"),
        ("right", "UMINUS"),
        ("right", "COMPLEMENT")
    )             # FIXME: set the correct precedence

    def p_name(self, p):
        """expr : IDENT"""
        p[0] = ast.ExpressionVar(p[1])

    def p_expression_int(self, p):
        """expr : NUMBER"""
        p[0] = ast.ExpressionInt(p[1])

    def p_expression_binop(self, p):
        """expr :  expr PLUS expr
                 | expr MINUS expr
                 | expr PRODUCT expr
                 | expr DIVISION expr
                 | expr MODULO expr
                 | expr AND expr
                 | expr OR expr
                 | expr XOR expr
                 | expr LSHIFT expr
                 | expr RSHIFT expr
                 """

        p[0] = ast.ExpressionBinOp(
            operator = self.BINOP[p[2]],
            left=p[1],
            right = p[3]
        )


    def p_expression_negation(self, p):
        """expr : MINUS expr %prec UMINUS"""
        p[0] = ast.ExpressionUniOp(
            operator = self.BINOP[p[1]],
            argument=p[2]
        )

    def p_expression_inversion(self, p):
        """expr : COMPLEMENT expr"""
        p[0] = ast.ExpressionUniOp(
            operator = self.BINOP[p[1]],
            argument=p[2]
        )

    def p_expression_parens(self, p):
        """expr : LPAREN expr RPAREN"""
        p[0] = p[2]



    def p_prgm(self, p):
        """prgm : DEF MAIN LPAREN RPAREN LCURLYBRACKET statement_star RCURLYBRACKET"""           
        p[0] = ast.Root(ast.Procedure("main", [], "int", p[6]))


    def p_statement_star(self, p):
        """statement_star :
                          | statement_star statement"""
        
        if len(p) == 1:
            p[0] = []
        else:
            p[0] = p[1]
            p[0].append(p[2])

    def p_statement(self, p):
        """statement : vardecl
                     | assign 
                     | print """

        p[0] = p[1]

    def p_vardecl(self, p):
        """vardecl : VAR IDENT EQUAL expr COLON INT SEMICOLON"""
    
        p[0] = ast.StatementVarDecl(p[2], p[6], p[4])

    def p_assign(self, p):
        """assign : IDENT EQUAL expr SEMICOLON"""

        p[0] = ast.StatementAssign(p[1], p[3])

    def p_print(self, p):
        """print : PRINT LPAREN expr RPAREN SEMICOLON"""

        p[0] = ast.StatementEval(ast.ExpressionCall("print", p[3]))



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



    ##DEFAULT STUFF from skeleton file, uncomment when parser is ready
    prgm = Parser.parse(prgm)

    if prgm is None:
        exit(1)

    print(prgm)

    # if not SynChecker.check(prgm):
    #     exit(1)

    # tac = MM.mm(prgm)

    # aout = [dict(
    #     proc = '@main',
    #     body = [x.tojson() for x in tac],
    # )]

    # try:
    #     with open(args.output, 'w') as stream:
    #         json.dump(aout, stream, indent = 2)
    #         print(file = stream) # Add a new-line

    # except IOError as e:
    #     print(f'cannot write outpout file {args.output}: {e}')
    #     exit(1)

# --------------------------------------------------------------------
if __name__ == '__main__':
    _main()
