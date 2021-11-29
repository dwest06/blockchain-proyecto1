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