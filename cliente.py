import socket
import random
import json
from p2pnetwork.node import Node
from wallet import Wallet

class Client(Node):

    def __init__(self, host, port, id=None, callback=None, max_connections=0, network_nodes={}):
        super().__init__(host, port, id=id, callback=callback, max_connections=max_connections)

        self.wallet = Wallet.generate_random_person()
        self.wallet.generate_keys()

        # Guarda el hash de la transaccion, index del bloque e index del gasto dentro de la transaccion
        # (index_block, hash_tx, index_gasto)
        self.utxo = []
        self.balance = 0

        # Select node to send data
        self.network_nodes = network_nodes
        self.node_name = random.choice(list(network_nodes.keys()))
        node = network_nodes[self.node_name]
        # Connect to node
        self.connect_with_node(node['host'], int(node['port']))
        print("Ready")

        self.refresh_balance()
    
    def refresh_balance(self):
        # Buscar en la blockchain sobre nuevas transacciones que se hayan realizado a esta billetera
        pass

    def generate_transaction(self, to, amount):

        if amount > self.balance:
            return False, "Monto mayor a balance"

        # Organizar las entradas y gastos de la transaccion

        transaction = {
            "sender": self.wallet.address,
            "reciever": "0x10527516238912",
            "amount": 10
        }
        data = {
            "message": 'transaccion_nueva',
            "data": transaction
        }
        data = json.dumps(data)
        data = self.wallet.sign_data(data) # Firmar el mensaje
        self.send_to_nodes(data)
    


def main(id, host, port, network):
    nodes = {}
    # open network file
    with open(network, 'r') as fd:
        n_nodes = fd.readline()
        for i in range(int(n_nodes)):
            node, port = fd.readline().rstrip().split(' ')
            nodes[node] = {
                "host": socket.gethostbyname(socket.gethostname()),
                "port": port,
                "connections": []
            }
        
        m_conn = fd.readline()
        for i in range(int(m_conn)):
            node1, node2 = fd.readline().rstrip().split(' ')
            nodes[node1]['connections'].append(node2)

    return Client(host, int(port), id, network_nodes=nodes)


