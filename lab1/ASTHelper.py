
#Global Variables that are gonna be important for generating the output TAC
registers = {} #keys are all gonna be numbers
output_json = []

###ALL of the helper classes that we'll use to represent the ACT content
class Root : 
    def __init__(self, procedure):
        self.procedure = procedure

    def TMM(self):
        #start by cleaning the global variables
        global registers
        global output_lines 

        registers = {}
        output_json = [{}]


        self.procedure.TMM()
        return output_json


    def __str__(self):
        return ("\n \nRoot : \n" + str(self.procedure) )


class Procedure: 
    def __init__(self, name, arguments, returntype, body):
        self.name = name
        self.arguments = arguments
        self.returntype = returntype
        self.body = body

    def TMM(self):
        global registers
        global output_json

        output_json[0]["proc"] = "main"
        output_json[0]["body"] = []

        for command in self.body : 
            command.TMM()

         


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

    def TMM(self):
        pass

    def __str__(self):
        return f"Declaring {self.name}"

class StatementAssign(Statement):
    def __init__(self, lvalue, rvalue):
        self.lvalue = lvalue
        self.rvalue = rvalue

    def TMM(self):
        pass

    def __str__(self):
        return f"{str(self.lvalue)} = {str(self.rvalue)}"

class StatementEval(Statement):
    def __init__(self, expression):
        self.expression = expression

    def TMM(self):
        pass

    def __str__(self):
        return str(self.expression)




class Expression:
    pass

class ExpressionCall(Expression):
    def __init__(self, target, argument):
        self.target = target
        self.argument = argument

    def TMM(self):
        pass

    def __str__(self):
        return f"Calling {self.target} with argument : {self.argument}"

class ExpressionVar(Expression):
    def __init__(self, name):
        self.name = name

    def TMM(self):
        pass

    def __str__(self):
        return self.name

class ExpressionInt(Expression):
    def __init__(self, value):
        self.value = value
    
    def TMM(self):
        pass

    def __str__(self):
        return str(self.value)

class ExpressionUniOp(Expression):
    def __init__(self, operator, argument):
        self.operator = operator
        self.argument = argument

    def TMM(self):
        pass

    def __str__(self):
        return f"({self.operator} {str(self.argument)})"

class ExpressionBinOp(Expression):
    def __init__(self, operator, left, right ):
        self.operator = operator
        self.left = left
        self.right = right
    
    def TMM(self):
        pass

    def __str__(self):
        return f"{str(self.left)} {self.operator} {str(self.right)}"




#The functions that will actually perform the job of converting the json to our custom AST format
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

