import hashlib

class Block():

    def __init__(self, index, transactions_list, timestamp, previous_block_hash, nonce=0):
        # No se si dejarlo ya que es el index de donde se ecuentre en la blockchain
        self.index = index
        self.previous_block_hash = previous_block_hash
        self.merkle_tree_root = None
        # Data
        self.block_data = "-".join(transactions_list) + "-" + previous_block_hash
        self.transactions_list = transactions_list
        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()
        self.timestamp = timestamp
        self.nonce = nonce


    def minar(self, difficulty):
        # Metodo para minar bloque
        
        hash = self.generate_hash()