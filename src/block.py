import hashlib
import random
from time import time
from pymerkle import MerkleTree


class Block():

    NONCE_LIMIT = 100000000000

    def __init__(self, transactions_list, previous_block_hash, difficulty):
        # Header
        self.previous_block_hash = previous_block_hash
        self.timestamp = time()
        self.difficulty = difficulty
        self.nonce = 0
        self.merkle_tree_root = self.merkle_tree(transactions_list)
        # Data
        self.transactions_list = transactions_list
        # self.index = index
        self.header_hash = self.mine(self.difficulty)


    def generate_hash(block_data):
        return hashlib.sha256((block_data).encode()).hexdigest()

    def mine(self, difficulty):
        block_header = self.previous_block_hash + str(self.timestamp) + str(difficulty) + self.merkle_tree_root
        hash_try = None

        while True:
            nonce = random.randint(0,self.NONCE_LIMIT)
            block_data =  block_header + str(nonce)
            hash_try = hashlib.sha256((block_data).encode()).hexdigest()
            if (hash_try.startswith(difficulty*'0')):
                self.nonce = nonce
                break

        return hash_try

    def merkle_tree(self, transactions_list):
        tree = MerkleTree(*transactions_list, hash_type='sha256', encoding='utf-8', raw_bytes=True, security=True)
        root = (tree.rootHash).decode('utf-8')
        return root