#Global Variables that are gonna be important for generating the output TAC
used_registers = [] #sorted list of all used temporaries
variable_lookup = {} #mapping token names to their register numbers

output_json = []


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
        "boolean-and":"",
        "boolean-or" : "",

        #comparison operators
        "less-than":"",
        "less-than-equal":"",
        "greater-than":"",
        "greater-than-equal" : "",

}


###SOME helper functions for interfacing between the global variables and the conversion functions
def add_entry(entry):
    global output_json

    output_json[0]["body"].append(entry)



def new_entry(opcode, argslist, register_num):
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


def new_free_register():

    global used_registers

    #first allocation
    if len(used_registers) == 0:
        used_registers.append(0)
        return 0

    #start by looking for gaps in allocated registers (ex : 1,3,4 -> 2)  
    for i in range(1, len(used_registers)):
        if (used_registers[i] - used_registers[i-1]) > 1:

            new_reg = used_registers[i] - 1

            used_registers = used_registers[:i] + [new_reg] + used_registers[i:]
            return new_reg


    #otherwise allocate new number
    new_reg = used_registers[-1] + 1
    used_registers.append(new_reg)
    return new_reg


def del_register(reg_num):
    global used_registers

    #do NOT allow deletion of variables, those should be deleted with a special function
    if reg_num in variable_lookup.values():
        return

    used_registers.remove(reg_num)




###ALL of the helper classes that we'll use to represent the ACT content
class Root : 
    def __init__(self, procedure):
        self.procedure = procedure

    def clean_slate():
        global registers
        global output_json

        registers = {}
        output_json = [{}]

    def TMM(self):
        #start by cleaning the global variables
        Root.clean_slate()

        self.procedure.TMM()
        return output_json

    def BMM(self):
        Root.clean_slate()

        self.procedure.BMM()
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
        global output_json

        output_json[0]["proc"] = "@main"
        output_json[0]["body"] = []

        for command in self.body : 
            command.TMM()

    def BMM(self):
        global output_json

        output_json[0]["proc"] = "@main"
        output_json[0]["body"] = []

        for command in self.body : 
            command.BMM()

        


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

    def TMM(self):
        global variable_lookup 

        reg = new_free_register()

        #initialize that register
        self.init.TMM(reg)

        #declare that register in the variable lookup
        variable_lookup[self.name] = reg


    def BMM(self):
        global variable_lookup

        #evaluate initialization value
        init_reg = self.init.BMM()

        #declare the variable to be that register
        variable_lookup[self.name] = init_reg


    def __str__(self):
        return f"Declaring {self.name}"


class StatementAssign(Statement):
    def __init__(self, lvalue, rvalue):
        self.lvalue = lvalue
        self.rvalue = rvalue #always an expression ?

    def TMM(self):
        #check that our variable (lvalue) name is in the lookup
        if not self.lvalue  in variable_lookup.keys():
            raise LookupError(f"Variable name {self.lvalue} used without being declared.")

        #if that's the case, store the result of the computation in it 
        var_reg = variable_lookup[self.lvalue]
        self.rvalue.TMM(var_reg)

    def BMM(self):
        #check that our variable (lvalue) name is in the lookup
        if not self.lvalue  in variable_lookup.keys():
            raise LookupError(f"Variable name {self.lvalue} used without being declared.")

        #now compute our rvalue
        rvalue_reg = self.rvalue.BMM()
        var_reg = variable_lookup[self.lvalue]

        #copy that value to the variable register
        add_entry(new_entry("copy", [f"%{rvalue_reg}"], var_reg))

        #delete the copied reg
        del_register(rvalue_reg)

             

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

    def TMM(self):
        #evaluate the argument
        argument_reg = new_free_register()
        self.argument.TMM(argument_reg)

        #call the function with that argument
        add_entry(new_entry(self.target, [f"%{argument_reg}"], -1) )

        #delete the temp register we used for the argument
        del_register(argument_reg)

    def BMM(self):
        #evaluate the argument
        arg_reg = self.argument.BMM()

        #call the function with that argument
        add_entry(new_entry(self.target, [f"%{arg_reg}"], -1))

        #delete the temp register
        del_register(arg_reg)


    def __str__(self):
        return f"Calling {self.target} with argument : {self.argument}"


class ExpressionVar(Expression):
    def __init__(self, name):
        self.name = name

    def TMM(self, target_reg):
        #start by getting the register number of our var
        if not self.name in variable_lookup.keys() :
            raise LookupError(f"Variable name {self.name} used without being declared.")
        
        var_reg = variable_lookup[self.name]

        #then copy that register value onto our target
        add_entry(new_entry("copy", [f"%{var_reg}"], target_reg))

    def BMM(self):
        if not self.name in variable_lookup.keys() :
            raise LookupError(f"Variable name {self.name} used without being declared.")

        return variable_lookup[self.name]

    def __str__(self):
        return self.name


class ExpressionInt(Expression):
    def __init__(self, value:int):
        self.value = value
        self.type = "int"
    
    def TMM(self, target_reg):
        #easy peasy
        add_entry(new_entry("const", [self.value], target_reg))

    def BMM(self):
        #store int in fresh register
        int_reg = new_free_register()
        add_entry(new_entry("const", [self.value], int_reg))

        return int_reg

    def __str__(self):
        return str(self.value)

class ExpressionBool(Expression):
    def __init__(self, value : bool):
        self.value = value

class ExpressionUniOp(Expression):
    def __init__(self, operator, argument):
        self.operator = operator
        self.argument = argument

    def TMM(self, target_reg):
        #evaluate argument
        arg_reg = new_free_register()
        self.argument.TMM(arg_reg)

        add_entry(new_entry(opcodes[self.operator], [f"%{arg_reg}"], target_reg))

        #delete temp reg
        del_register(arg_reg)

    def BMM(self):
        #evaluate argument 
        arg_reg = self.argument.BMM()
        result_reg = new_free_register()

        add_entry(new_entry(opcodes[self.operator], [f"%{arg_reg}"], result_reg))

        del_register(arg_reg)
        return result_reg


    def __str__(self):
        return f"({self.operator} {str(self.argument)})"


class ExpressionBinOp(Expression):
    def __init__(self, operator, left, right ):
        self.operator = operator
        self.left = left
        self.right = right
    
    def TMM(self, target_reg):
        #evaluate arguments
        left_reg  = new_free_register()
        right_reg = new_free_register()

        self.left.TMM(left_reg)
        self.right.TMM(right_reg)

        add_entry(new_entry(opcodes[self.operator], [f"%{left_reg}", f"%{right_reg}"], target_reg))

        #delete temps regs
        del_register(left_reg)
        del_register(right_reg)


    def BMM(self):
        left_reg = self.left.BMM()
        right_reg = self.right.BMM()

        result_reg = new_free_register()
        add_entry(new_entry(opcodes[self.operator], [f"%{left_reg}", f"%{right_reg}"], result_reg))


        del_register(left_reg)
        del_register(right_reg)

        return result_reg


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





###WE DEFINE THE MAXIMAL MUNCH OBJECTS HERE
class TMM():
    def __init__(self, root : Root):
        #creating all of the important variables
        self.used_registers = [] 
        self.variable_lookup = {}

        self.output_json = []

        #storing the root ast object
        self.root = root

    def TMM(self, node):
        #process the current node and add the appropriate tac code lines
        pass


    def get_TAC_json(self):
        return self.output_json