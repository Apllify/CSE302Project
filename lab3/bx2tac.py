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


#TODO : add line number support for ast classes 

class Lexer:


    reserved = {
        "print" : "PRINT",
        "int" : "INT",
        "var" : "VAR",

        "def" : "DEF",
        "main" : "MAIN",

        #control flow stuff
        "if": "IF",
        "else":"ELSE",
        "while": "WHILE",
        "break":"BREAK",
        "continue" : "CONTINUE"

    }

    tokens = (                 
        'IDENT' ,
        'NUMBER',

        #arithmetic operators
        'PLUS'  ,
        "MINUS",
        "PRODUCT",
        "DIVISION",
        "MODULO",

        #bitwise operators
        "AND",
        "OR",
        "XOR",
        "LSHIFT",
        "RSHIFT",
        "COMPLEMENT",

        "EQUAL",

        #boolean terminals
        "TRUE",
        "FALSE",

        #boolean operators
        "ANDBOOL",
        "ORBOOL",
        "NOTBOOL",

        #comparison operators
        "LESSTHAN",
        "LESSTHANEQUAL",
        "GREATERTHAN",
        "GREATERTHANEQUAL",

        "ISEQUAL",
        "NOTEQUAL",


        #punctuation
        "COLON",
        "SEMICOLON",

        #brackets
        "LPAREN",
        "RPAREN",
        "LCURLYBRACKET",
        "RCURLYBRACKET"

    ) + tuple(reserved.values())

    #characters to skip 
    t_ignore = " \t\f\v"


    # simple definitions should start with t_

    #arithmetic operators
    t_PLUS = re.escape('+') 
    t_MINUS = "-"
    t_PRODUCT = re.escape("*")
    t_DIVISION = re.escape("/")
    t_MODULO = re.escape("%")

    #bitwise operators
    t_AND = re.escape("&")
    t_OR = re.escape("|")
    t_XOR = re.escape("^")
    t_LSHIFT = re.escape("<<")
    t_RSHIFT = re.escape(">>")
    t_COMPLEMENT = re.escape("~")

    t_EQUAL = re.escape("=")

    #boolean terminals
    t_TRUE = re.escape("true")
    t_FALSE = re.escape("false")

    #boolean operators
    t_ANDBOOL = re.escape("&&")
    t_ORBOOL = re.escape("||")
    t_NOTBOOL = re.escape("!")

    #comparison operators
    t_LESSTHAN = re.escape("<")
    t_LESSTHANEQUAL = re.escape("<=")
    t_GREATERTHAN = re.escape(">")
    t_GREATERTHANEQUAL = re.escape(">=")

    t_ISEQUAL = re.escape("==")
    t_NOTEQUAL = re.escape("!=")

    #punctuation
    t_COLON = re.escape(":")
    t_SEMICOLON = re.escape(";")


    #brackets
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

        "!" : "boolean-not",

    }

    BINOP = {
        #arithmetic operators
        '+'  : 'addition'           ,
        '-'  : 'subtraction'        ,
        '*'  : 'multiplication'     ,
        '/'  : 'division'           ,
        '%'  : 'modulus'            ,

        #bitwise operators
        '>>' : 'logical-right-shift',
        '<<' : 'logical-left-shift' ,
        '&'  : 'bitwise-and'        ,
        '|'  : 'bitwise-or'         ,
        '^'  : 'bitwise-xor'        ,

        #boolean operators
        "&&" : "boolean-and",
        "||" : "boolean-or",

        #comparison operators
        "<" : "less-than",
        "<=" : "less-than-equal",
        ">" : "greater-than",
        ">=" : "greater-than-equal"


    }

    tokens = Lexer.tokens
    
    start = 'prgm'

    precedence = (
        #boolean operators
        ("left", "ORBOOL"),
        ("left", "ANDBOOL"),

        #bitwise operators
        ("left", "OR"),
        ("left", "XOR"),
        ("left", "AND"),

        #comparison operators
        ("nonassoc", "ISEQUAL", "NOTEQUAL"),
        ("nonassoc", "LESSTHAN", "LESSTHANEQUAL", "GREATERTHAN", "GREATERTHANEQUAL"),

        #bitwise shifts
        ("left", "LSHIFT", "RSHIFT"),

        #normal arithmetic operators
        ("left",   "PLUS", "MINUS"),
        ("left", "PRODUCT", "DIVISION", "MODULO"),

        #most urgent (unary) operators
        ("right", "UMINUS"),
        ("right", "COMPLEMENT")
    )             

    def p_name(self, p):
        """expr : IDENT"""
        p[0] = ast.ExpressionVar(p[1])

    def p_expression_int(self, p):
        """expr : NUMBER"""
        p[0] = ast.ExpressionInt(p[1])

    def p_expression_bool(self, p):
        """expr : TRUE
                | FALSE"""
        boolean = (True if p[1] == "true" else False)
        p[0] = ast.ExpressionBool(boolean)



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
                 | expr ANDBOOL expr
                 | expr ORBOOL expr
                 | expr LESSTHAN expr
                 | expr LESSTHANEQUAL expr
                 | expr GREATERTHAN expr
                 | expr GREATERTHANEQUAL expr
                 | expr ISEQUAL expr
                 | expr NOTEQUAL expr
                 """

        p[0] = ast.ExpressionBinOp(
            operator = self.BINOP[p[2]],
            left=p[1],
            right = p[3]
        )


    def p_expression_negation(self, p):
        """expr : MINUS expr %prec UMINUS"""
        p[0] = ast.ExpressionUniOp(
            operator = self.UNIOP[p[1]],
            argument=p[2]
        )

    def p_expression_uniop(self, p):
        """expr : COMPLEMENT expr
                | NOTBOOL expr   """
        p[0] = ast.ExpressionUniOp(
            operator = self.UNIOP[p[1]],
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
                     | print 
                     | ifelse
                     | while"""

        p[0] = p[1]

    def p_vardecl(self, p):
        """vardecl : VAR IDENT EQUAL expr COLON INT SEMICOLON"""
    
        p[0] = ast.StatementVarDecl(p[2], p[6], p[4])

    def p_assign(self, p):
        """assign : IDENT EQUAL expr SEMICOLON"""

        p[0] = ast.StatementAssign(p[1], p[3])

    def p_ifelse(self, p):
        """ifelse : IF LPAREN expr RPAREN LCURLYBRACKET statement_star RCURLYBRACKET ifrest"""
        
        p[0] = ast.StatementIfElse(p[3], p[6], p[8])

    def p_print(self, p):
        """print : PRINT LPAREN expr RPAREN SEMICOLON"""

        p[0] = ast.StatementEval(ast.ExpressionCall("print", p[3]))




    def p_ifrest(self, p):
        """ifrest : 
                  | ELSE ifelse 
                  | ELSE LCURLYBRACKET statement_star RCURLYBRACKET"""
        
        if len(p) == 1:
            p[0] = ast.StatementIfRest()
        elif len(p) == 3:
            p[0] = ast.StatementIfRest(ifelse = p[2])
        elif len(p) == 5:
            p[0] = ast.StatementIfRest(block = p[3])

    def p_while(self, p):
        """while : WHILE LPAREN expr RPAREN LCURLYBRACKET statement_star RCURLYBRACKET"""
        p[0] = ast.StatementWhile(p[3], p[6])


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

    error_types = (
        "ERROR",
        "WARNING",
        "INFO"
    )

    base_functions = (
        "print",
    ) 

    max_num_bit_length = 63

    def __init__(self):
        self.declared_variables = []
        self.declared_functions = [] + list(SynChecker.base_functions)

        self.error_log = []
        self.n_errors = 0

        self.stmt_number = 1

    def error_mes(self, type, content, stmt_i = -1):

        sane_type = type.upper()
        if sane_type not in SynChecker.error_types : 
            sane_type = "ERROR"

        if stmt_i == -1:
            self.error_log.append(f"{sane_type} : {content.capitalize()}.")
        else:
            self.error_log.append(f"Statement n°{stmt_i} : {sane_type} : {content.capitalize()}")
        self.n_errors += 1

    

    def sort_error_log(self):
        #the order should go "Errors -> Warnings -> Infos"
        sort_key = lambda x : len(SynChecker.error_types) - SynChecker.error_types.index(x.split(" ")[3]) 
        self.error_log.sort(key=sort_key)


    def for_program(self, root:ast.Root):
        # START by checking that the procedure (function) of our program
        # is called main and has no arguments
        if root.procedure.name != "main":
            self.error_mes("ERROR", "main function not named 'main'")

        if root.procedure.arguments != []:
            self.error_mes("ERROR", "main function shouldn't take any arguments")

        #now perform syntax checking line by line
        for statement in root.procedure.body : 
            self.for_statement(statement)
            self.stmt_number += 1

        #TODO : delete me once debugging is over
        self.sort_error_log()
        print(self.error_log)
        
        
    def for_statement(self, stmt:ast.Statement):

        match stmt : 
            case ast.StatementVarDecl(name = name, init = expression) : 

                #check that this is our first time declaring this 
                if name in self.declared_variables : 
                    self.error_mes("WARNING", f"variable {name} declared more than once", self .stmt_number)

                #check that the expression is valid without having declared the var
                self.for_expression(expression)

                #declare the var
                if  name not in self.declared_variables : 
                    self.declared_variables.append(name)

            case ast.StatementAssign(lvalue = lvalue, rvalue= rvalue):
                #check that the variable we're assigning to exists
                if  lvalue not in self.declared_variables : 
                    self.error_mes("ERROR", f"variable {lvalue} used before declaration", self.stmt_number) 

                #check on the expression
                self.for_expression(rvalue)

            case ast.StatementEval(expression = expression):
                self.for_expression(expression)

            case _:
                self.error_mes("ERROR", "unrecognized statement type", self.stmt_number)



    def for_expression(self, expr:ast.Expression):
        match expr : 
            case ast.ExpressionCall(target=target,argument=argument):
                #check that the called function is valid
                if target not in self.declared_functions :
                    self.error_mes("ERROR", f"function {target} undefined", self.stmt_number)

                #TODO : allow for argument lists
                if type(argument) == type([]): 
                    raise Exception("lists of arguments not supported yet :(")
                
                self.for_expression(argument)

            case ast.ExpressionVar(name=name):

                if name not in self.declared_variables :
                    self.error_mes("ERROR", f"variable {name} used before declaration", self.stmt_number)

            case ast.ExpressionInt(value=value):

                if value.bit_length() > SynChecker.max_num_bit_length:
                    self.error_mes("ERROR", f"value {value} exceeds the {SynChecker.max_num_bit_length} bit limit", self.stmt_number)

            case ast.ExpressionUniOp(argument = arg):
                self.for_expression(arg)

            case ast.ExpressionBinOp(left =left, right = right):
                self.for_expression(left)
                self.for_expression(right)     

            # case _: 
            #     self.erorr_mes("ERROR", "unsupported expression type", self.stmt_number)





    @classmethod
    def check(cls, prgm : ast.Root):
        checker = cls()
        checker.for_program(prgm)
        return (checker.n_errors == 0)




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

    print("woo everything worked ?")


    # if not SynChecker.check(prgm):
    #     exit(1)

    # #TODO : add option to choose between tmm and bmm (both already implemented)
    # tac = prgm.TMM()

    # try:
    #     with open(args.output, 'w') as stream:
    #         json.dump(tac, stream, indent = 2)
    #         print(file = stream) # Add a new-line

    # except IOError as e:
    #     print(f'cannot write output file {args.output}: {e}')
    #     exit(1)

# --------------------------------------------------------------------
if __name__ == '__main__':
    _main()
