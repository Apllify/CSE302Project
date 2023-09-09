import sys 
import json
from ASTHelper import * #the file that holds all of our object form json

"""
FLAWS that I should eventually fix : 
- Call expression only handles one expression at the moment
--> In order to refactor, you need to change both its class representation to have a list
--> But also its TMM method that only assumes that one argument is present 
"""





if __name__ == "__main__" : 
    
    cmd_inputs = sys.argv

    json_file_path = ""
    json_object = None

    flag = "tmm"

    output_filepath = ""
    output_filepath_index = 2



    if len(cmd_inputs) == 1:
        raise Exception("Argument Error : No source file path provided.")
    





        
    #load the ast json file
    json_file_path = cmd_inputs[1]
    try : 
        with open(json_file_path, "r") as ast_file:
            json_object = json.load(ast_file)
    except: 
        raise Exception("File Error : Provided Json file could not be loaded.")

    #get the input flag
    if cmd_inputs[2][0] == "-":

        output_filepath_index = 3
        
        input_flag = cmd_inputs[2][1:]
        while input_flag[0] == "-":
            input_flag = input_flag[1:]  


        if input_flag in ("tmm", "bmm"):
            flag = input_flag
        else:
            raise Exception("Argument Error : Unrecognized flag.")



    #load the output filepath
    output_filepath = cmd_inputs[output_filepath_index]


    #check that we haven't been given too many arguments
    if len(cmd_inputs) > (output_filepath_index + 1):
        print("Warning : Too many arguments provided, ignoring all extra arguments.")


    #convert the json file to a better format
    ast_object = json_to_AST(json_object, True)


    #now run the command that's gonna generate (only tmm supported for now)
    if flag == "tmm":
        TAC_code_lines, errors = ast_object.TMM()
        TAC_json = json.dumps(TAC_code_lines)
    else:
        raise Exception("BMM not supported yet :(")

 
    #write the result to the output file :D
    with open(output_filepath, "w") as file:
        file.write(TAC_json)



    #this should be at the verrrry end of the conversion
    print("\n \nConversion succesful !")
    print("-----------------DONE----------------- \n \n")






