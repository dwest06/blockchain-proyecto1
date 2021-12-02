import hashlib
import random
from time import time
from pymerkle import MerkleTree

from transaction import Transaction


class Block():

    NONCE_LIMIT = 100000000000

    def __init__(self, transactions_list, previous_block_hash, difficulty):
        # Header
        self.previous_block_hash = previous_block_hash
        self.timestamp = time()
        self.difficulty = difficulty
        self.nonce = 0
        self.merkle_tree_root = self.merkle_tree(self.transactions_data(transactions_list))
        # Data
        self.index = None
        self.transactions_list = transactions_list
        self.hash = None


    def generate_hash(block_data):
        return hashlib.sha256((block_data).encode()).hexdigest()

    def mine(self):
        """
        Method for mine block
        """
        block_header = str(self.previous_block_hash) + str(self.timestamp) + str(self.difficulty) + self.merkle_tree_root
        hash_try = None

        while True:
            nonce = random.randint(0,self.NONCE_LIMIT)
            block_data =  block_header + str(nonce)
            hash_try = hashlib.sha256((block_data).encode()).hexdigest()
            if (hash_try.startswith(self.difficulty * '0')):
                self.nonce = nonce
                self.hash = hash_try
                break
        # Guardar el hash 
        if hash_try:
            return True
        return False

    def verify(self):
        """
        Method for verify the nonce is the correct for this block
        """
        block_header = self.previous_block_hash + str(self.timestamp) + str(self.difficulty) + self.merkle_tree_root
        block_data = block_header + str(self.nonce)
        hash_try = hashlib.sha256((block_data).encode()).hexdigest()
        if (hash_try.startswith(self.difficulty * '0')) and hash_try == self.block_hash:
            return True
        return False

    def transactions_data(self, transactions_list):
        return list(map(lambda tx: tx.hash, transactions_list))


    def merkle_tree(self, transactions_data_list):
        # TODO: Quitar esto cuando se haga lo del Coinbase
        if not transactions_data_list:
            return '1234'
        tree = MerkleTree(*transactions_data_list, hash_type='sha256', encoding='utf-8', raw_bytes=True, security=True)
        root = (tree.rootHash).decode('utf-8')
        return root

    @classmethod
    def from_dict(cls, dict):
        transactions = [Transaction.from_dict(tx) for tx in dict['transactions_list']]
        block = cls(transactions, dict['previous_block_hash'], dict['difficulty'])
        block.timestamp = dict['timestamp']
        block.nonce = dict['nonce']
        block.merkle_tree_root = dict['merkle_tree_root']
        block.hash = dict['hash']
        block.index = dict['index']
        return block

    def to_dict(self):
        return {
            'previous_block_hash' : self.previous_block_hash,
            'timestamp' : self.timestamp,
            'difficulty' : self.difficulty,
            'nonce' : self.nonce,
            'merkle_tree_root' : self.merkle_tree_root,
            'transactions_list' : [ tx.to_dict() for tx in self.transactions_list],
            'hash' : self.hash,
            'index' : self.index,
        }