import sys 
import json
from ASTHelper import * #the file that holds all of our object form json

"""
FLAWS that I should eventually fix : 
- Call expression only handles one expression at the moment
"""





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


    #now run the command that's gonna generate (only tmm supported for now)
    if flag == "tmm":
        TAC_code_lines = ast_object.TMM()
 


    #this should be at the verrrry end of the conversion
    print("\n \nConversion succesful !")
    print("-----------------DONE----------------- \n \n")






