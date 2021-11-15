import hashlib
from time import time

class Transaction:

    def __init__(self, sender, reciever, amount):
        self.sender = sender
        self.reciever = reciever
        self.amount = amount
        self.timestamp = time()
        # ????
        # self.hash

    def valid(self):
        return True


class Block():

    def __init__(self, index, transactions_list, timestamp, previous_block_hash, nonce=0):
        # No se si dejarlo ya que es el index de donde se ecuentre en la blockchain
        self.index = index
        self.previous_block_hash = previous_block_hash
        # Data
        self.block_data = "-".join(transactions_list) + "-" + previous_block_hash
        self.transactions_list = transactions_list
        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()
        self.timestamp = timestamp
        self.nonce = nonce

    def minar(self, difficulty):
        # Metodo para minar bloque
        
        hash = self.generate_hash()


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



