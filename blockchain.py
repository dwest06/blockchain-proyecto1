from hashlib import sha256
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

    def minar(self, difficulty):
        # Metodo para minar bloque
        
        hash = self.generate_hash()


class BlockChain():

    def __init__(self, difficulty):
        pass


    def minar(self, bloque: Block):
        # Minar el bloque
        result = bloque.minar(self.difficutly)

        return result



