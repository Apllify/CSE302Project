import sys 
import json

"""
FLAWS that I should eventually fix : 
- Call expression only handles one expression at the moment
"""


###ALL of the helper classes that we'll use to represent the ACT content
class Root : 
    def __init__(self, procedure):
        self.procedure = procedure

    def __str__(self):
        return ("\n \nRoot : \n" + str(self.procedure) )


class Procedure: 
    def __init__(self, name, arguments, returntype, body):
        self.name = name
        self.arguments = arguments
        self.returntype = returntype
        self.body = body

    def __str__(self):
        child_outputs = []
        for command in self.body : 
            child_outputs.append(str(command))

        output = "Procedure lines : \n" + "\n".join(child_outputs)
        return output

        

class Statement : 
    pass

class StatementVarDecl(Statement):
    def __init__(self, name, type, init):
        self.name = name
        self.type = type
        self.init = init

    def __str__(self):
        return f"Declaring {self.name}"

class StatementAssign(Statement):
    def __init__(self, lvalue, rvalue):
        self.lvalue = lvalue
        self.rvalue = rvalue

    def __str__(self):
        return f"{str(self.lvalue)} = {str(self.rvalue)}"

class StatementEval(Statement):
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        return str(self.expression)




class Expression:
    pass

class ExpressionCall(Expression):
    def __init__(self, target, argument):
        self.target = target
        self.argument = argument

    def __str__(self):
        return f"Calling {self.target} with argument : {self.argument}"

class ExpressionVar(Expression):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class ExpressionInt(Expression):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class ExpressionUniOp(Expression):
    def __init__(self, operator, argument):
        self.operator = operator
        self.argument = argument

    def __str__(self):
        return f"({self.operator} {str(self.argument)})"

class ExpressionBinOp(Expression):
    def __init__(self, operator, left, right ):
        self.operator = operator
        self.left = left
        self.right = right

    def __str__(self):
        return f"{str(self.left)} {self.operator} {str(self.right)}"



def json_to_name(js_obj):
    return js_obj[1]['value']

def json_to_type(js_obj):
    return js_obj[0]




def json_to_AST(json_obj, is_root = False):
    

    #the root object is special and doesn't have a name
    if (is_root):
        return Root(json_to_AST(json_obj["ast"][0]))

    #otherwise cycle through the names
    obj_type = json_obj[0]

    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa")
    print(obj_type)
    if obj_type == "<decl:proc>":

        name = json_to_name(json_obj[1]["name"])
        arguments = json_obj[1]["arguments"]
        return_type = json_obj[1]["returntype"]
        body = json_obj[1]["body"]

        #parse the contents of body
        parsed_body = []
        for command in body:
            parsed_body.append(json_to_AST(command)) 

        return Procedure(name, arguments, return_type, parsed_body)

    elif obj_type == "<statement:vardecl>":
        name = json_to_name(json_obj[1]["name"])
        type = json_to_type(json_obj[1]["type"])
        init = json_to_AST(json_obj[1]["init"])

        return StatementVarDecl(name, type, init)

    elif obj_type == "<statement:assign>":
        lvalue = json_to_name(json_obj[1]["lvalue"][1]["name"])
        rvalue = json_to_AST(json_obj[1]["rvalue"])

        return StatementAssign(lvalue, rvalue)

    elif obj_type == "<statement:eval>":

        expression = json_to_AST(json_obj[1]["expression"])

        return StatementEval(expression)

    elif obj_type == "<expression:call>":
        target = json_to_name(json_obj[1]["target"])
        argument = json_to_AST(json_obj[1]["arguments"][0])

        return ExpressionCall(target, argument)


    elif obj_type == '<expression:var>':
        return ExpressionVar(json_to_name(json_obj[1]['name']))

    elif obj_type == '<expression:int>':
        return ExpressionInt(json_obj[1]['value'])
        
    elif obj_type == '<expression:uniop>':
        operator = json_to_name(json_obj[1]['operator'])
        argument = json_to_AST(json_obj[1]['argument']) 
        return ExpressionUniOp(operator, argument)

    elif obj_type == '<expression:binop>':
        operator = json_to_name(json_obj[1]["operator"])
        left = json_to_AST(json_obj[1]["left"])
        right = json_to_AST(json_obj[1]["right"])
        return ExpressionBinOp(operator, left, right)

    else:

        #if no option was identified, raise an error
        raise ValueError(f'Unrecognized <expression>: {json_obj[0]}')


if __name__ == "__main__" : 
    
    cmd_inputs = sys.argv
    filepath_index = 1

    json_file_path = ""
    json_object = None
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
    json_file_path = cmd_inputs[filepath_index]
    try : 
        with open(json_file_path, "r") as ast_file:
            json_object = json.load(ast_file)
    except: 
        raise Exception("File Error : Provided Json file could not be loaded.")


    #convert the json file to a better format
    ast_object = json_to_AST(json_object, True)
    print(str(ast_object))

    #this should be at the verrrry end of the conversion
    print("\n \nConversion succesful !")
    print("-----------------DONE----------------- \n \n")






