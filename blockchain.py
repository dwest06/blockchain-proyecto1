from block import Block
from transaction import Transaction

class BlockChain():

    def __init__(self):
        # Set difficulty to 5 for test
        self.difficulty = 5
        self.chain = []

    def create_genesis_block(self, address):
        # A function to generate genesis block and appends it to the chain.
        # TODO: Generate Coinbase transaction
        transactions = []
        genesis_block = Block(transactions, '000000', self.difficulty)
        genesis_block.mine()
        # print(f"Genesis Block: {genesis_block.to_dict()}")
        return genesis_block

    def change_transaction_status(self, block: Block):
        """
        Metodo para cambiar el estatus de las transacciones dentro del bloque minado
        ademas de cambiar las UTXO de Unspend a Spend
        """
        for tx in block.transactions_list:
            tx.estado = True
            for entrada in tx.entradas:
                back_tx = self.search_tx_by_hash(entrada.tx_hash_ref)
                for gasto in back_tx.gastos:
                    if gasto.reciever == entrada.sender and gasto.amount == entrada.amount:
                        gasto.detail = 'spend'
                        break

    def generate_block(self, transaction_list):
        """
        Generate Block
        """
        block = Block(transaction_list, self.get_last_block().hash, self.difficulty)
        return block

    def get_last_block(self):
        return self.chain[-1]

    def minar(self, bloque: Block):
        # Minar el bloque
        return bloque.mine()

    def verify_block(self, bloque: Block):
        # Minar el bloque
        return bloque.verify()
        
    def validate_transaction(self, transaction: Transaction) -> bool:
        # Coinbase validation
        if transaction.coinbase:
            return True

        # Validate amounts
        if not transaction.validate_amounts():
            return False

        # Validar que cada entrada corresponde a un Gasto anterior
        valid = False
        for entrada in transaction.entradas:
            valid = False 

            back_tx = self.search_tx_by_hash(entrada.tx_hash_ref)
            for gasto in back_tx.gastos:
                if gasto.reciever == entrada.sender and gasto.amount == entrada.amount:
                    valid = True # Si nunca entra aqui es que la entrada no fue verificada
                    break
            
            if not valid:
                return False
        
        return True

    def addBlock(self, new_block):
        self.chain.append(new_block)
        return len(self.chain) - 1

    # SEARCH BLOCK

    def search_block_by_hash(self, hash: str):
        for i in reversed(self.chain):
            if hash == i.hash:
                return i
        return None

    def search_block_by_index(self, index: int):
        if index > len(self.chain):
            return False
        return self.chain[index]
        

    # SEARCH TRANSACTION

    def search_tx_by_hash(self, hash, index: int = None):
        if index:
            block = self.search_block_by_index(index)
            for t in block.transactions_list:
                if t.hash == hash:
                    return t
        else:
            for block in self.chain.reverse():
                for t in block.transactions_list:
                    if t.hash == hash:
                        return t