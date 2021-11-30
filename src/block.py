import hashlib
from pymerkle import *


class Block():

    def __init__(self, index, transactions_list, timestamp, previous_block_hash, difficulty, nonce=0):
        # Header
        self.previous_block_hash = previous_block_hash
        self.timestamp = timestamp
        self.difficulty = difficulty
        self.nonce = nonce
        self.NONCE_LIMIT = 100000000000
        self.merkle_tree_root = self.merkle_tree(transactions_list)
        # Data
        self.transactions_list = transactions_list
        self.index = index
        self.header_hash = self.mine(self.difficulty)


    def generate_hash(block_data):
        return hashlib.sha256((block_data).encode()).hexdigest()

    def mine(self, difficulty):
        for self.nonce in range (self.NONCE_LIMIT):

            block_data = self.previous_block_hash + self.timestamp + str(difficulty) + self.merkle_tree_root + str(self.nonce)
            hash_try = hashlib.sha256((block_data).encode()).hexdigest()
            
            print(f"\nIntento de hash con nonce: {self.nonce}")
            print(f"\nHash : {hash_try}")
            
            if (hash_try.startswith(difficulty*'0')):
                return hash_try

    def merkle_tree(self, transactions_list):
        tree = MerkleTree(*transactions_list, hash_type='sha256', encoding='utf-8', raw_bytes=True, security=True)
        root = (tree.rootHash).decode('utf-8')
        return root
