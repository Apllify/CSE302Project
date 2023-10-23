class Jump :

    jump_types = [
        "jmp",

        "jl", "jle",
        "jnl", "jnle",
        "jz", "jnz"
    ]

    def __init__(self, jump_type, args = []):

        if jump_type not in Jump.jump_types:
            raise SyntaxError(f"Command {jump_type} not a recognized jump")

        self.jump_type = jump_type
        self.args = args


class Block: 
    def __init__(self, entry_label, content):
        self.entry_label = entry_label
        self.content = content

class CFG : 
    def __init__(self, block_list, edges : dict[tuple[int, int], Jump] ):
        """
        edges is a mapping of the form  
        (i1, i2) -> jump3

        where i1, i2 are indexes of elements in block_list
        jump3 is an instance of the jump class
        """

        self.block_list = block_list
        self.edges = edges
        
    def add_block(self, block):
        self.block_list.append(block)

    def get_edge(self, i1, i2):
        self.edges.get((i1, i2))
    
    def preds(self, i):
        """
        Get the predecessors of a block
        """
        predecessors = []

        for couple in self.edges :
            if couple[1] == i:
                predecessors.append(couple[0])

        return predecessors

    def succs(self, i):
        """
        Get the successors of a block
        """

        successors = []

        for couple in self.edges :
            if couple[0] == i:
                successors.append(couple[1])

        return successors


def TAC_command(opcode, args, result_reg=-1):
    """
    Generates the dict corresponding to a single TAC command
    """
    #generate the fields of an entry
    entry = {}
    entry["opcode"] = opcode
    entry["args"]  = args

    #-1 target registry is code for "discard result"
    if result_reg >= 0 :
        entry["result"] = f"%{result_reg}"
    else:
        entry["result"] = None

    return entry


def TAC2Blocks(TAC_dict):
    """
    Assumes the only procedure is the main procedure
    input : the dictionary form of a tac program
    output : a list of block type elements 
    """
    body = TAC_dict[0]["body"]

    #find/add entry label if applicable
    if body[0]["opcode"] != "label":
        entry_label = TAC_command("label", ["%.Lentry"], -1)
    else : 
        entry_label = body[0]
        body = body[1:]

    #start by adding all the blocks WITHOUT the edges
    all_blocks = []
    cur_block = Block(entry_label, [])
    i=0 

    while i < len(body) :
        command = body[i]
        opcode = command["opcode"]

        if opcode in Jump.jump_types:
            #eat up all successor jump commands, then finish block
            cur_block.content.append(command)

            while i < len(body):
                next_command = body[i+1]
            
            

        elif opcode == "ret":
            #end the conversion
            cur_block.content.append(command)
            all_blocks.append(cur_block)
            break

        elif opcode == "label":
            #do something
            pass
        else : 
            cur_block.content.append(command)

        i += 1




if __name__ == "__main__":
    # <-- parse command line arguments here 
    pass