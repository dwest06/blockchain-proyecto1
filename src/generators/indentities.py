import argparse
from ..node import Node
from ..wallet import Wallet

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


if __name__ == "__main__":

    # Leer los parametros
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', type=int, help='Numero de indentidades')
    parser.add_argument('-n', type=int, help='Numero de Nodos')
    args = parser.parse_args()
    # access to arguments
    # print(args.f, args.n, args.d)
    generator = Identities.generate_indetities(args.i, args.n)