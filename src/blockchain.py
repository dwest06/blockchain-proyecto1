from .block import Block

class BlockChain():

    def __init__(self):
        # Set difficulty to 4 for test
        self.difficulty = 4
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        # A function to generate genesis block and appends it to the chain.
        # Generate Coinbase transaction
        transactions = []
        genesis_block = Block(transactions, '00000000', self.difficulty)
        genesis_block.mine()
        return genesis_block

    def get_last_block(self):
        return self.chain[-1]


    def minar(self, bloque: Block):
        # Minar el bloque
        result = bloque.mine(self.difficulty)
        return result

    def addBlock(self, new_block):
        # Creo que esto no hace falta aqui
        # new_block.previous_block_hash = self.get_last_block().block_hash
        # new_block.mine(self.difficulty)

        self.chain.appen(new_block)

    def search_block_by_hash(self, hash: str):
        for i in reversed(self.chain):
            if hash == i.hash:
                return i
        return None

    def search_block_by_index(self, index: int):
        if index > len(self.chain):
            return False
        return self.chain[index]
        