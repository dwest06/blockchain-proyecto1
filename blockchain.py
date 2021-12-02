from block import Block

class BlockChain():

    def __init__(self):
        # Set difficulty to 4 for test
        self.difficulty = 4
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        # A function to generate genesis block and appends it to the chain.
        # TODO: Generate Coinbase transaction
        transactions = []
        genesis_block = Block(transactions, '000000', self.difficulty)
        print(f"Genesis Block: {genesis_block}")
        genesis_block.mine()
        return genesis_block

    def generate_block(self, transaction_list):
        """
        Generate Block
        """
        return Block(transaction_list, self.get_last_block().hash, self.difficulty)

    def get_last_block(self):
        return self.chain[-1]

    def minar(self, bloque: Block):
        # Minar el bloque
        return bloque.mine()

    def verify_block(self, bloque: Block, nonce, difficulty, block_hash):
        # Minar el bloque
        return bloque.verify(nonce, difficulty, block_hash)
        

    def addBlock(self, new_block):
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
        