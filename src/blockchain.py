from .block import Block

class BlockChain():

    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        # A function to generate genesis block and appends it to the chain. The block has index 0, previous_block_hash as 0, and a valid hash.
        genesis_block = Block(0, [], 0, "0", 1)
        # genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[len(self.chain)-1]


    def minar(self, bloque: Block):
        # Minar el bloque
        result = bloque.mine(self.difficulty)

        return result

    def addBlock(self, new_block):
        new_block.previous_block_hash = self.get_last_block().block_hash
        new_block.mine(self.difficulty)

        self.chain.appen(new_block)
