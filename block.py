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
        self.merkle_tree_root = self.merkle_tree(self.transactions_data_list)
        # Data
        self.transactions_list = transactions_list
        self.transactions_data_list = self.transactions_data()
        # self.index = index
        self.header_hash = self.mine()


    def generate_hash(block_data):
        return hashlib.sha256((block_data).encode()).hexdigest()

    def mine(self):
        """
        Method for mine block
        """
        start = time()
        block_header = self.previous_block_hash + self.timestamp + str(self.difficulty) + self.merkle_tree_root
        hash_try = None

        while True:
            nonce = random.randint(0,self.NONCE_LIMIT)
            block_data =  block_header + str(nonce)
            hash_try = hashlib.sha256((block_data).encode()).hexdigest()
            if (hash_try.startswith(self.difficulty * '0')):
                self.nonce = nonce
                break
        
        print(f"Minado en {time() - start} seg")
        # Guardar el hash 
        if hash_try:
            self.hash = hash_try
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

    def transactions_data(self):
        transactions_data_list = []

        for tx in self.transactions_list:
            transactions_data_list.append(tx.hash)

        return transactions_data_list

    def merkle_tree(self, transactions_data_list):
        # TODO: Revisar esto, porque en teoria deberia llegar son los hash de las transacciones
        # Ademas de que siempre deberia existir al menos una transaccion en la lista de transacciones
        # Que vendria siendo la coinbase
        if not transactions_data_list:
            return '1234567890'
        tree = MerkleTree(*transactions_data_list, hash_type='sha256', encoding='utf-8', raw_bytes=True, security=True)
        root = (tree.rootHash).decode('utf-8')
        return root


    @classmethod
    def from_dict(cls, dict):
        pass