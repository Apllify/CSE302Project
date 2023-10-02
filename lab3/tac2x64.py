import argparse
import json


#TODO :
# - currently this prgrm assumes that there is ONLY one method/procedure and that it is called main
# - this program also assumes that the input is syntactically correct (no references before declare, etc...)

def gen_asm(tac_json, output_path):

    asm_lines = []


    #get the three important components from the json file
    command_list = tac_json[0]["body"]
    temps = tac_json[0]["temps"]
    labels = tac_json[0]["labels"]

    #matches each temp names (ex : %1) to its offset from rbp (starting from -1, and decreasing by one each time)
    temps_lookup = dict(zip(temps, range(-1, -len(temps)-1, -1) ) )


    #helper function to simplify adding INDENTED lines of asm
    def add_asm(opcode, arg1 = "", arg2 = ""):

        nonlocal asm_lines 

        indent = "\t"

        if arg1 == "" and arg2 == "":
            new_line = f"{opcode}"
        elif arg2 == "":
            new_line = f"{opcode} {arg1}"
        else :
            new_line = f"{opcode} {arg1}, {arg2}"

        asm_lines.append(indent + new_line)

    
    #helper function to obtain the string address of a given temporary
    def get_temp_address(tempname):

        if (tempname == None):
            return None

        return f"{8*temps_lookup[tempname]}(%rbp)"


    #gives a readable string from a TAC op
    def op_to_string(op):
        opcode = command['opcode']
        args = map(str, command['args'])
        result = command['result']

        #case 1 : op with no return value
        if result == None:
            return_string = f"{opcode} {' '.join(args)}"
        #case 2 : op that stores result somewhere
        else:
            return_string = f"{result} = {opcode} {' '.join(args)}"

        return return_string




    #boilerplate code
    asm_lines.append("\t.globl main")
    asm_lines.append("\t.text")

    asm_lines.append("main:")

    add_asm("pushq", r"%rsp")
    add_asm("movq", r"%rsp", r"%rbp")

    asm_lines += "", ""


    #allocate the appropriate amount of temporaries on the stack, remaining 16-Byte aligned
    num_temps = len(temps) + (len(temps)%2)
    num_bytes_alloc = num_temps * 8 
    add_asm("subq", f"${num_bytes_alloc}", r"%rsp")

    #adding empty lines for style
    asm_lines += "", "" 



    #process the code line by line now
    simple_binops = {
        "add": "addq",
        "sub": "subq",
        "and": "andq",
        "or": "orq",
        "xor": "xorq",
        }

    special_binops = ("mul", "div", "mod", "shl", "shr")

    uniops = {
        "neg": "negq",
        "not" : "notq"
    }

    cond_jumps = [
        "jz", "jl", "jle",
        "jnz", "jnl", "jnle"
    ]


    for command in command_list:
        #####---------------------------------------
        #####BIG BLOCK of code incoming

        opcode = command['opcode']
        args = command['args']

        result = command['result']
        result_address = get_temp_address(result)

        #start by adding the source command as a comment
        asm_lines.append(f"\t/* {op_to_string(command)} */")


        #now add the actual code line 
        if opcode == "nop":

            pass

        elif opcode == "const":

            constant = args[0]
            add_asm("movq", f"${constant}", result_address)

        elif opcode == "copy":

            #move first value to r11
            #then move the r11 value into the result variable
            source_address = get_temp_address(args[0])

            add_asm("movq", source_address, r"%r11")
            add_asm("movq", r"%r11", result_address)

        elif opcode in simple_binops.keys() :

            #move s1 to r11
            #opcode s2 to r11
            #move r11 to result address
            asm_op = simple_binops[opcode]

            s1_address = get_temp_address(args[0])
            s2_address = get_temp_address(args[1])

            add_asm("movq", s1_address, r"%r11")
            add_asm(asm_op, s2_address, r"%r11")
            add_asm("movq", r"%r11", result_address)


        elif opcode in special_binops :
            pass

        elif opcode in uniops : 
            
            asm_op = uniops[opcode]
            source_address = get_temp_address(args[0])

            add_asm("movq", source_address, r"%r11")
            add_asm(asm_op, r"%r11")
            add_asm("movq", r"%r11", result_address)

        elif opcode == "jmp":
            destination = args[0]
            add_asm(opcode, destination)

        elif opcode in cond_jumps : 
            condition = get_temp_address(args[0])
            destination = args[1]

            add_asm(opcode, condition, destination)

        elif opcode == "label":
            
            label_name = args[0][1:]
            
            #determine whether local or global label
            if label_name[0] == ".":
                asm_lines.append(f".main{label_name}:")
            else: 
                asm_lines.append(f"{label_name}:")



        elif opcode == "print":
            
            source = get_temp_address(args[0])

            add_asm("movq", source, r"%rdi")
            add_asm("callq", "bx_print_int")


            

        else: 
            print(opcode)
            raise NotImplementedError()


        #empty line
        asm_lines.append("")


        #####BIG BLOCK of code over
        #####---------------------------------------



    asm_lines += "", ""



    #punctuate the assembly program
    add_asm("movq", r"%rbp", r"%rsp")
    add_asm("popq", r"%rbp")
    add_asm("movq", r"$0", r"%rax")
    add_asm("retq")

    #write everything to the output file 
    with open(output_path, "w") as output_file : 
        output_file.write( "\n".join(asm_lines) )  



    
    






if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog = "tac2x64")
    parser.add_argument("input", help = "input file (.tac.json)")
    args = parser.parse_args()

    try :
        with open(args.input, "r") as input_file:
            tac_string = input_file.read()
    except:
        raise Exception("Error : Invalid input filename provided !")

    output_file = args.input.split(".")[0] + ".s"

    tac_json = json.loads(tac_string)

    gen_asm(tac_json, output_file)