from time import time
import names
import random
import gnupg
from blockchain import BlockChain, Block, Transaction

gpg = gnupg.GPG()
PASSPHRASE = "dg123456"

class Wallet(): # cambiar nombre a Wallet

    def __init__(self, name: str, lastname: str, email: str):
        self.name = name
        self.lastname = lastname
        self.email = email

    def get_full_name(self) -> str:
        return f"{self.name} {self.lastname}"

    @classmethod
    def generate_random_person(cls):
        name = names.get_first_name()
        last = names.get_last_name()
        email = f"{name}-{last}{random.randint(0,999)}@testmail.com"
        return cls(name, last, email)

    def generate_keys(self):
        # https://gist.github.com/ryantuck/56c5aaa8f9124422ac964629f4c8deb0
        # Generate key
        input_data = gpg.gen_key_input(
            name_real = self.get_full_name(),
            name_email=self.email,
            passphrase=PASSPHRASE,
        )
        key = gpg.gen_key(input_data)
        self.pk = gpg.export_keys(key.fingerprint)
        self.sk = gpg.export_keys(key.fingerprint, True, passphrase=PASSPHRASE)

    def __str__(self):
        return self.get_full_name()


class Node():

    def __init__(self, node_number: int, blockchain = None, pool_transactions = None):
        self.number = node_number
        self.blockchain = blockchain
        self.pool_transactions = pool_transactions
        self.adjacent_nodes = []

    def mine(self, difficulty):
        # Encontrar un hash que cumpla con la dificultad
        pass

    
    def enter_transaction(self, remitente, transaction: Transaction):
        # Validar la Transaccion
        if not transaction.valid():
            return {"message": "transaccion nueva", "remitente": remitente, "estado": "No"}

        # Agregar la transaccion al pool de transacciones

        # Retornar ACK del mensaje

        return {"message": "transaccion nueva", "remitente": remitente, "estado": "Si"}

    def presentation(self, new_node):
        # Identificar nodo

        # Agregar nuevo nodo a la lista de nodos adyacentes

        return {"message": "transaccion nueva", "remitente": new_node}


    def propagate_transaction(self):
        # Enviar la transaccion a los nodos adyacentes
        for i in self.adjacent_nodes:
            # Send transaccion
            pass

        return 

    def propagte_candidate_block(self, block):
        # Validar que no se ha verificado
        if block in self.blockchain:
            return 

        # Enviar bloque a los nodos adyacentes
        for i in self.adjacent_nodes:
            # Send node
            pass
        
        return


    def __str__(self):
        return f"Node{self.number}"


class Identities():
    # Directorio de identidades
    
    def __init__(self):
        self.num_identities = 0
        self.num_nodes = 0

    @classmethod
    def generate_indetities(cls, num_identities: int, num_nodes: int):
        identities = cls()
        identities.num_identities = num_identities
        identities.num_nodes = num_nodes

        # Dict for storing identities
        wallets = {}
        for i in range(num_identities):
            # Generar identidades random
            person = Wallet.generate_random_person()
            # Crear claves
            person.generate_keys()
            # Save person
            wallets[person.email] = person
        
        identities.wallets = wallets

        nodes = []
        # Nodes
        for i in range(num_nodes):
            node = Node(i)
            nodes.append(node)

        identities.nodes = nodes
