class Jump :

    jump_types = [
        "jmp",

        "jl", "jle",
        "jnl", "jnle",
        "jz", "jnz"
    ]

    def __init__(self, jump_type, arg = []):
        if jump_type not in jump_types:
            raise SyntaxError(f"Command {jump_type} not a recognized jump")

        self.jump_type = jump_type
        self.arg = arg


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


def TAC2Blocks(TAC_dict):
    """
    input : the dictionary form of a tac program
    output : a list of block type elements 
    """
    pass




if __name__ == "__main__":
    # <-- parse command line arguments here 
    pass