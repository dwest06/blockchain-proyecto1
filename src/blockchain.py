from .block import Block

class BlockChain():

    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.chain = []

    def create_genesis_block(self):
        # A function to generate genesis block and appends it to the chain. The block has index 0, previous_block_hash as 0, and a valid hash.
        genesis_block = Block(0, [], 0, "0")
        # genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    def minar(self, bloque: Block):
        # Minar el bloque
        result = bloque.minar(self.difficutly)

        return result