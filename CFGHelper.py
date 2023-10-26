class Jump :

    conditional_jumps = [
        "jl", "jle",
        "jnl", "jnle",
        "jz", "jnz"
    ]

    # normal jump : jmp

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


class TAC2Blocks:
    """
    Assumes the only procedure is the main procedure
    input : the dictionary form of a tac program
    output : a list of block type elements 
    """

    def __init__(self, TAC_dict):
        self.TAC_dict = TAC_dict
        self.body = TAC_dict[0]["body"]
        self.reserved_labels=  TAC_dict[0]["labels"]

        self.label_count = 0

        self.all_blocks = []


    #new label, prefixed with 
    def new_label(self):
        """
        Returns fresh new label of the form %.La[number]
        TODO : For now assumes that all tac label names only contain numerics
        """
        label_name = f"%.LA{self.label_count}"
        self.label_count += 1
        return label_name
        



    def convert(self):
        #find/add entry label if applicable
        if self.body[0]["opcode"] != "label":
            entry_label = TAC_command("label", [self.new_label()], -1)
        else : 
            entry_label = self.body[0]
            self.body = self.body[1:]

        #start by adding all the blocks WITHOUT the edges
        cur_block = Block(entry_label, [])
        i=0 

        while i < len(self.body) :
            command = self.body[i]
            opcode = command["opcode"]

            if opcode in Jump.conditional_jumps:
                #if the last command in block was also a cond jump just add
                if (True):
                    cur_block.content.append(command)
                else: 
                    #otherwise create new block with new label and add ourselves to it
                    self.all_blocks.append(cur_block)
                    cur_block = CFG([], dict()) 
                    cur_block.content.append(TAC_command("label", [self.new_label()], -1))
                    cur_block.content.append(command)



            elif opcode == "jmp":

                

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