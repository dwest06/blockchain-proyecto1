import hashlib
import random

class Transaccion():
    def __init__(self, from_addres, to_addres, amount):
        self.from_addres = from_addres
        self.to_addres = to_addres
        self.amount = amount

class GenerarTransaccion ():
    def __init__(self, archivo_config):

        # Leer archivo y retornar:

        self.frecuencia = 0
        self.NumEntradasMin = 0
        self.NumEntradasMax = 0
        self.NumSalidasMin = 0
        self.NumSalidasMax = 0

        # DUDA: Entender bien Numero de entradas min/max y numero de salidas min/max

    def IdentidadRandom(identidad_dict):
        identidad_generada = email, person = random.choice(list(identidad_dict.items()))
        return person

    def genTransaction ():
        from_addres = IdentidadRandom(identidad_dict).addres
        to_addres = IdentidadRandom(identidad_dict).addres

        while from_addres == to_addres:
            # Volver a generar identidades random
            from_addres = IdentidadRandom(identidad_dict).addres
            to_addres = IdentidadRandom(identidad_dict).addres

        amount = random(0, from_addres.amount())


class Block:
    def __init__(self, index, transactions_list, timestamp, previous_block_hash, nonce=0):
        self.index = index
        self.transactions_list = transactions_list
        self.timestamp = timestamp
        self.previous_block_hash = previous_block_hash
        self.block_data = "-".join(transactions_list) + "-" + previous_block_hash
        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()
        self.nonce = nonce



    # def compute_hash(self):
    #   #A function that return the hash of the block contents.
    #   block_string = json.dumps(self.__dict__, sort_keys=True)
    #   return hashlib.sha256(self.block_data.encode()).hexdigest()


class Blockchain:
    # difficulty of our PoW algorithm
    difficulty = 2

    def __init__(self):
        self.unconfirmed_transactions_list = []
        self.chain = []

    def create_genesis_block(self):
        # A function to generate genesis block and appends it to the chain. The block has index 0, previous_block_hash as 0, and a valid hash.
        genesis_block = Block(0, [], 0, "0")
        # genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)