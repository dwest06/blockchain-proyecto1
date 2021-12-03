from block import Block
from transaction import Transaction

class BlockChain():

    def __init__(self, difficulty, recompensa):
        # Set difficulty
        self.difficulty = difficulty
        self.recompensa = recompensa
        self.chain = []

    def generate_coinbase(self, address):
        return Transaction.generate_coinabse(address)

    def create_genesis_block(self, address):
        # A function to generate genesis block and appends it to the chain.
        tx = self.generate_coinbase(address)
        transactions = [tx]
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
            if tx.coinbase:
                continue
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
        block = Block(transaction_list, self.get_last_block_hash(), self.difficulty)
        return block

    def get_last_block_hash(self):
        if self.chain:
            return self.chain[-1].hash
        # TODO: PQC
        return '0000000000'

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
        index = len(self.chain) - 1
        new_block.index = index
        return index

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
            for block in reversed(self.chain):
                for t in block.transactions_list:
                    if t.hash == hash:
                        return t


    def to_dict(self):
        return {
            "difficulty": self.difficulty,
            "recompensa": self.recompensa,
            "chain": [ block.to_dict() for block in self.chain ]
        }

    @classmethod
    def from_dict(cls, dict):
        bc = cls(dict['difficulty'], dict['recompensa'])
        bc.chain = [ Block.from_dict(block) for block in dict['chain']]
        return bc