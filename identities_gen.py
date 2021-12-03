import argparse
import json
from node import Node, NodeConfig
from wallet import Wallet
from subprocess import call

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

        wallet_json = {}
        for i in range(num_identities):
            # Generar identidades random
            person = Wallet.generate_random_person()
            # Crear claves
            person.generate_keys()
            # Save person
            wallets[person.email] = person
            wallet_json[person.email] = {
                "full_name": person.get_full_name(),
                "address": person.address
            }
            print(f"Generating wallet {i}")
        with open('wallets.json', 'w+') as file:
            text = json.dumps(wallet_json)
            file.write(text)

        # Guardar Wallets
        identities.wallets = wallets

        nodes = []

        # Nodes
        for i in range(num_nodes):
            print(f"Generating node {i}")
            call(['gnome-terminal', '-e', f"python3 node.py -n nodo{i} -d . -f archivo_red.txt -c node_config.yaml"])
            nodes.append({"name":f"node{i}"})

        identities.nodes = nodes

        print(f"GENERATED {len(identities.wallets)} WALLETS AND {len(identities.nodes)} NODES ")

if __name__ == "__main__":

    # Leer los parametros
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', type=int, help='Numero de indentidades')
    parser.add_argument('-n', type=int, help='Numero de Nodos')
    args = parser.parse_args()
    # access to arguments
    # print(args.f, args.n, args.d)
    generator = Identities.generate_indetities(args.i, args.n)