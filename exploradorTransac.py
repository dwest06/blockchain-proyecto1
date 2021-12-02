import socket
import random
import argparse
import json
from p2pnetwork.node import Node

class TransacExplorer(Node):

    def __init__(self, host, port, id=None, callback=None, max_connections=0, network_nodes={}):
        super().__init__(host, port, id=id, callback=callback, max_connections=max_connections)

        # Select node to send data
        self.network_nodes = network_nodes
        self.node_name = random.choice(list(network_nodes.keys()))
        node = network_nodes[self.node_name]
        # Connect to node
        self.connect_with_node(node['host'], int(node['port']))
        print("Ready")

    def explorar_hash(self, hash):
        data = json.dumps({"message": "transaction_explorer", "data": hash})
        self.send_to_nodes(data)

    def node_message(self, node, data):
        from pprint import pprint
        pprint(data)


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

    return TransacExplorer(host, int(port), id, network_nodes=nodes)


if __name__ == "__main__":

    # Leer los parametros
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-a', type=str, help='Altura del Block')
    parser.add_argument('-h', type=str, help='Hash del Bloque')
    args = parser.parse_args()

    explorer = main('Explorer1', '127.0.0.1', 15100, 'archivo_red.txt')
    explorer.start()

    if args.a:
        explorer.explorar_altura(args.a)
    else:
        explorer.explorar_hash(args.h)
