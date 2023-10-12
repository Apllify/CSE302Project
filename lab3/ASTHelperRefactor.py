###ALL of the helper classes that we'll use to represent the ACT content
class Root : 
    def __init__(self, procedure):
        self.procedure = procedure

    def clean_slate():
        global registers
        global output_json

        registers = {}
        output_json = [{}]

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

        
class Name : 
    def __init__(self, name):
        self.name = name

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
        self.rvalue = rvalue #always an expression ?
             

    def __str__(self):
        return f"{str(self.lvalue)} = {str(self.rvalue)}"



class StatementEval(Statement):
    def __init__(self, expression):
        self.expression = expression

    def TMM(self):
        self.expression.TMM()

    def BMM(self):
        self.expression.BMM()

    def __str__(self):
        return str(self.expression)



class StatementIfElse(Statement):
    def __init__(self, condition, block, ifrest):
        self.condition = condition
        self.block = block
        self.ifrest = ifrest

class StatementIfRest(Statement):
    def __init__(self, ifelse=None, block=None):
        # only ONE of these two attributes can have a 
        # non-null value for a given instance
        self.ifelse =  ifelse
        self.block = block

class StatementWhile(Statement):
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block


class Expression:
    #can take values : "int" / "bool"
    type = None

    #returns the type of the expression while minimizing computation
    def get_type(self):
        if self.type != None:
            return self.type
        else:
            self.compute_type()
            return self.type

    #should be overridden by every single expression child
    def compute_type(self):
        raise NotImplementedError()


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
    def __init__(self, value:int):
        self.value = value
        self.type = "int"

    def __str__(self):
        return str(self.value)


class ExpressionBool(Expression):
    def __init__(self, value : bool):
        self.value = value


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









###WE DEFINE THE MAXIMAL MUNCH OBJECTS HERE
class TMM():

    opcodes = {
            #arithmetic operators
            "addition": "add",
            "subtraction" : "sub",
            "multiplication": "mul",
            "division": "div",
            "modulus" : "mod",
            "opposite": "neg",

            #bitwise operators
            "bitwise-xor": "xor",
            "bitwise-or" : "or",
            "bitwise-and": "and",
            "logical-left-shift":"shl",
            "logical-right-shift":"shr",
            "bitwise-negation":"not",

            #boolean operators
            "boolean-and":"and",
            "boolean-or" : "or",

            #comparison operators
            "less-than":"lt",
            "less-than-equal":"lte",
            "greater-than":"gt",
            "greater-than-equal" : "gte",

    }



    def __init__(self):
        #creating all of the important variables
        self.used_registers = [] 
        self.label_counter = 0

        #list of scopes of variables
        #each variable lookup maps "varname -> (var_reg, var_type)"
        self.variable_scopes = [{}]

        self.output_json = []





    ###START OF HELPER functions###
    def add_entry(self, entry):
        self.output_json[0]["body"].append(entry)


    def new_entry(self, opcode, argslist, register_num):
        #generate the fields of an entry
        entry = {}
        entry["opcode"] = opcode
        entry["args"]  = argslist

        #-1 target registry is code for "discard result"
        if register_num >= 0 :
            entry["result"] = f"%{register_num}"
        else:
            entry["result"] = None

        return entry

    def new_label(self):
        raise NotImplementedError()

    def new_free_register(self):


        #first allocation
        if len(self.used_registers) == 0:
            self.used_registers.append(0)
            return 0

        #start by looking for gaps in allocated registers (ex : 1,3,4 -> 2)  
        for i in range(1, len(self.used_registers)):
            if (self.used_registers[i] - self.used_registers[i-1]) > 1:

                new_reg = self.used_registers[i] - 1

                self.used_registers = self.used_registers[:i] + [new_reg] + self.used_registers[i:]
                return new_reg


        #otherwise allocate new number
        new_reg = self.used_registers[-1] + 1
        self.used_registers.append(new_reg)
        return new_reg

    def del_register(self, reg_num):

        #do NOT allow deletion of variables, those should be deleted with a special function
        if reg_num in self.variable_lookup.values():
            return

        self.used_registers.remove(reg_num)

    def add_variable(self, var_name, var_reg, var_type):
        self.variable_scopes[-1][var_name] = (var_reg, var_type)


    def find_variable(self, var_name):
        """returns : a tuple of the form (var_reg, var_type)"""
        #look through scope from narrowest to broadest
        for scope in self.variable_scopes[::-1]:
            if var_name in scope.keys():
                return scope[var_name]

        raise NameError(f"Variable name {var_name} used without being declared")

        
    
    def compute_type(self, node:Expression):
        """Computes the type of the input node, and stores it in its type field"""

        #no need to compute if the type is already known
        try : 
            if node.type != None :
                return 
        except:
            return

        





    
    ###END OF HELPER functions###



    def TMM(self, root:Root):
        #clean everything before starting the TMM
        self.used_registers = []
        self.output_json = {}
        self.variable_lookup = ()

        self.TMM_node(root.procedure)



    def TMM_node(self, node, result_reg = -1):
        
        #proceed by case by case analysis over the node types
        match node : 

            case Procedure(name = _, arguments = _, returntype=_, body=body) :
                output_json[0]["proc"] = "@main"
                output_json[0]["body"] = []

                for node in body : 
                    self.TMM_node(node)

            case StatementVarDecl(name =name, type=type, init=init):
                reg = self.new_free_register()

                self.TMM_node(init, reg)
                self.add_variable(name, reg, type)
                
            case StatementAssign(lvalue = lvalue, rvalue=rvalue):
                var_reg = self.find_variable(lvalue)[0]

                var_reg = self.variable_lookup[lvalue]
                self.TMM_node(rvalue, var_reg)

            case StatementEval(expression=expression):
                self.TMM_node(expression)

            case StatementIfElse(condition=condition, block = block, ifrest=ifrest):
                raise NotImplementedError()

            case StatementIfRest(ifelse=ifelse, block=block):
                raise NotImplementedError()

            case StatementWhile(condition=condition, block=block):
                raise NotImplementedError()

            case ExpressionCall(target=target, argument=argument):
                argument_reg = self.new_free_register()
                
                self.TMM_node(argument, argument_reg)

                self.add_entry(self.new_entry(target, [f"%{argument_reg}"], -1))
                self.del_register(argument_reg)

            case ExpressionVar(name=name):

                var_reg = self.find_variable(name)[0]

                self.add_entry(self.new_entry("copy", [f"%{var_reg}"], result_reg))

            case ExpressionInt(value=value):
                self.add_entry(self.new_entry("const", [value], result_reg))

            case ExpressionBool(value=value):
                raise NotImplementedError()

            case ExpressionUniOp(operator=operator, argument=argument):
                arg_reg = self.new_free_register()
                self.TMM_node(argument, arg_reg)

                self.add_entry(self.new_entry(self.opcodes[operator], [f"%{arg_reg}"], result_reg))

                self.del_register(arg_reg)

            case ExpressionBinOp(operator=operator,left=left,right=right):
                left_reg = self.new_free_register()
                right_reg= self.new_free_register()

                self.TMM_node(left, left_reg)
                self.TMM_node(right, right_reg)

                self.add_entry(self.new_entry(self.opcodes[operator], [f"%{left_reg}", f"%{right_reg}"], result_reg))

                self.del_register(left_reg)
                self.del_register(right_reg)


            case _ :
                raise NotImplementedError("Unrecognized AST object in ast2tac")

    def TMM_node_bool(self, node, l1, l2):
        raise NotImplementedError()
            


    def get_TAC_json(self):
        return self.output_json




#The functions that will actually perform the job of converting the json to our custom AST format
def json_to_name(js_obj):
    return js_obj[1]['value']

def json_to_type(js_obj):
    return js_obj[0]




def json_to_AST(json_obj, is_root = False):
    """!Deprecated!"""    

    #the root object is special and doesn't have a name
    if (is_root):
        return Root(json_to_AST(json_obj["ast"][0]))

    #otherwise cycle through the names
    obj_type = json_obj[0]

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
