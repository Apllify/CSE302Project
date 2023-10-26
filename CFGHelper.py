class Block: 
    def __init__(self, entry_labels=None, content=None, exits=None):
        #entry labels is special, instead of storing full TAC commands, 
        #it only stores the label names 
        self.entry_labels = entry_labels if entry_labels else [] 
        self.content = content if content else []
        self.exits = exists if exits else []

    def __str__(self):
        br = "\n"
        string_content = list(map(str, self.content))
        return f"Entry Labels : {self.entry_labels} \nContent : \n {(br.join(string_content)) }\nExit commands : {self.exits}\n\n"

class CFG : 

    def __init__(self, block_list=[], edges=[]):
        """
        edges is a mapping of the form  
        (i1, i2) -> [jump1, jump2, jump3]

        where i1, i2 are indexes of elements in block_list
        jumpN are all tac commands with opcode == jmp or cond_jmp 
        """

        self.block_list = block_list
        self.edges = edges

        self.labelid_dict = dict() #maps (label) -> (id) 

    def label_to_id(self, label):
        """
        Finds the internal id of a block from one of its entry labels.
        Returns : An int if there is a match, "None" otherwise
        """

        #check if we've already computed this value before
        query = self.labelid_dict.get(label)
        if query : 
            return query

        #otherwise manually search through all of our blocks
        for i, block in enumerate(self.block_list):
            if label in block.entry_labels :
                self.labelid_dict[label] = i
                return i 

        #no match found 
        return None

    def get_edge(self, i1, i2):
        """
        Returns None if no edge exists
        """
        self.edges.get((i1, i2))


    def add_edge(self, jmp_tac, i1, i2):
        if self.get_edge(i1, i2): 
            self.edges[(i1, i2)].append(jmp_tac)
        else : 
            self.edges[(i1, i2)] = [jmp_tac]

    def add_edge_hybrid(self, jmp_tac, i1, L2):
        """
        Actually quite useful in the context of this program.
        If no block matches L2, then doesn't do anything
        """
        i2 = self.label_to_id(L2)
        if i2 :
            self.add_edge(jmp_tac, i1, i2)


        

    
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
    if result_reg != -1 :
        entry["result"] = f"%{result_reg}"
    else:
        entry["result"] = None

    return entry


class TAC2CFG:
    """
    Assumes the only procedure is the main procedure
    input : the dictionary form of a tac program
    output : a list of block type elements 
    """

    conditional_jumps = [
        "jl", "jle",
        "jnl", "jnle",
        "jz", "jnz"
    ]

    def __init__(self, TAC_dict):
        self.TAC_dict = TAC_dict
        self.body = TAC_dict[0]["body"]
        self.reserved_labels=  TAC_dict[0]["labels"]

        self.label_count = 0

        self.all_blocks = []
        self.CFG = CFG()


    #new label, prefixed with 
    def new_label(self):
        """
        Returns fresh new label of the form %.La[number]
        TODO : For now assumes that all tac label names only contain numerics
        """
        label_name = f"%.LA{self.label_count}"
        self.label_count += 1
        return label_name
        



    def convert_naive(self):
        """
        Generates a list of all the correct CFG blocks,
        Does not generate the CFG graph itself 
        """

        #start with an empty block,
        #all blocks will be progressively added to the full list
        cur_block = Block()

        i = 0
        while i < len(self.body) :

            command = self.body[i]
            opcode = command["opcode"]


            #check whether our current block is still in labelling phase
            if cur_block.content == [] and cur_block.exits == []:
                if opcode == "label" :
                    #add only the label name
                    cur_block.entry_labels.append(command["args"][0])
                    
                    i += 1
                    continue

                else : 
                    #make sure there is at least one entry label
                    if len(cur_block.entry_labels) == 0:
                        cur_block.entry_labels.append(self.new_label())




            #check for non-linear instruction
            if opcode in TAC2CFG.conditional_jumps :

                cur_block.exits.append(command)
              


            elif opcode == "jmp" :

                #move on to new block
                cur_block.exits.append(command)
                self.all_blocks.append(cur_block)
                cur_block = Block()

            else : 

                #FROM here on, we need to make sure that there are no trailing conditionals
                #(since we can't follow them up)
                if cur_block.exits != [] or opcode == "label" : 

                    #check if we need to add an explicit jump-through
                    if len(cur_block.exits) == 0  or cur_block.exits[-1]["opcode"] in TAC2CFG.conditional_jumps :
                        
                        jump_label_to_add = []
                        if opcode == "label" :
                            jump_label = command["args"][0]
                        else : 
                            jump_label = self.new_label()
                            jump_label_to_add.append(jump_label)
                        
                        cur_block.exits.append(TAC_command("jmp", [jump_label]))

                        self.all_blocks.append(cur_block)
                        cur_block = Block(jump_label_to_add)
                        continue

                    else : 
                        self.all_blocks.append(cur_block)
                        cur_block = Block()
                        continue

                

                if opcode == "ret" :
                    #check that no other exits before this 
                    cur_block.exits.append(command)
                    self.all_blocks.append(cur_block)
                    cur_block = Block()


                else : 
                    #guaranteed to have a linear instruction
                    cur_block.content.append(command)

            i += 1

    def connect_blocks(self):
        """
        Uses the block list created by convert naive
        to generate a proper CFG
        """
        #TODO TODO TODO : implement me !
        self.CFG.block_list = self.all_blocks



    def create_CFG(self):
        #start by creating all of the blocks independently
        self.convert_naive()

        #merge them 
        self.connect_blocks()

        return self.CFG

        





if __name__ == "__main__":
    #DEBUG CODE
    fib = [dict()]
    body = []

    body.append(TAC_command("const", [10], "n"))
    body.append(TAC_command("const", [0], 0))
    body.append(TAC_command("const", [1], 1))
    body.append(TAC_command("const", [1], 2))
    body.append(TAC_command("label", ["%.L1"]))
    body.append(TAC_command("jz", ["%n", "%.L3"]))
    body.append(TAC_command("label", ["%.L2"]))
    body.append(TAC_command("sub", ["%n", "%2"], "n"))
    body.append(TAC_command("add", ["%0", "%1"], 3))
    body.append(TAC_command("copy", ["%1"], 0))
    body.append(TAC_command("copy", ["%3"], 1))
    body.append(TAC_command("jmp", ["%.L1"]))
    body.append(TAC_command("label", ["%.L3"]))


    body.append(TAC_command("ret", ["%0"]))

    fib[0]["body"] = body
    fib[0]["labels"] = []


    #run our cfg on it 
    converter = TAC2CFG(fib)
    converter.convert()
    for block in converter.all_blocks:
        print(block)
        print()



