import sys 
import json


###ALL of the helper classes that we'll use to represent the ACT content
class Root : 
    def __init__(self, procedure):
        self.procedure = procedure

class Procedure: 
    def __init__(self, name, arguments, returntype, body):
        self.name = name
        self.arguments = arguments
        self.returntype = returntype
        self.body = body

        

class Statement : 
    pass

class StatementVarDecl(Statement):
    def __init__(self, name, type, init):
        self.name = name
        self.type = type
        self.init = init

class StatementAssign(Statement):
    def __init__(self, lvalue, rvalue):
        self.lvalue = lvalue
        self.rvalue = rvalue

class StatementEval(Statement):
    def __init__(self, expression):
        self.expression = expression




class Expression:
    pass

class ExpressionCall(Expression):
    def __init__(self, target, argument):
        self.target = target
        self.argument = argument

class ExpressionVar(Expression):
    def __init__(self, name):
        self.name = name

class ExpressionInt(Expression):
    def __init__(self, value):
        self.value = value

class ExpressionUniOp(Expression):
    def __init__(self, operator, argument):
        self.operator = operator
        self.argument = argument

class ExpressionBinOp(Expression):
    def __init__(self, operator, left, right ):
        self.operator = operator
        self.left = left
        self.right = right




def json_to_AST(json_obj):
    pass


if __name__ == "__main__" : 
    
    cmd_inputs = sys.argv
    filepath_index = 1

    ast_file_path = ""
    ast_json_object= None
    flag = "tmm"


    if len(cmd_inputs) == 1:
        raise Exception("Argument Error : No file path provided.")
    
    #case where we received an execution flag
    if cmd_inputs[1][:2] == "--":

        filepath_index = 2
        input_flag = cmd_inputs[1][2:]

        if input_flag in ("tmm", "bmm"):
            flag = input_flag
        else:
            raise Exception("Argument Error : Unrecognized flag.")

    #check that we haven't been given too many arguments
    if len(cmd_inputs) > (filepath_index + 1):
        print("Warning : Too many arguments provided, ignoring all extra arguments.")

        
    #now finally load the ast json file
    ast_file_path = cmd_inputs[filepath_index]
    try : 
        with open(ast_file_path, "r") as ast_file:
            ast_json_object = json.load(ast_file)
    except: 
        raise Exception("File Error : Provided Json file could not be loaded.")



    #this should be at the verrrry end of the conversion
    print("\n \n-----------------DONE-----------------")
    print("Conversion succesful ! \n \n")






