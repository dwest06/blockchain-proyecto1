import argparse
import socket
from time import sleep
from random import randint
from p2pnetwork.node import Node
import yaml

class TransactionGenerator(Node):

    sleep_time = 60
    max_iterations = 10

    def __init__(self, frecuencia, ent_min, ent_max, sal_min, sal_max, nodos, dir, host, port) -> None:
        super().__init__(host, port, id="GeneradorTransacciones")
        # Configs
        self.frecuencia = frecuencia
        self.ent_min = ent_min
        self.ent_max = ent_max
        self.sal_min = sal_min
        self.sal_max = sal_max
        # States Node
        self.nodos = nodos
        self.dir = dir

    def generate_transaction(self, _from, _to, amount):
        # Generar la transaccion con la sintaxis de P2SH
        pass

    def send_transaction(self, node, transaction):
        # Send transaction to node 
        pass

    def start_generator(self):
        iteration = 0
        while True:
            # For test only max_iterations are valids
            if iteration >= self.max_iteration:
                break
            
            # send transactions
            for i in range(self.frecuencia):
                # Buscar address de in y addres de out en el directorio
                addr_in = '123456'
                addr_out = '098765'
                amount = 1000
                transaction = self.generate_transaction(addr_in, addr_out, amount)
                # Search and send to node
                index = randint(0, len(self.nodes))
                node = self.nodes[index]
                self.send_transaction(node, transaction)



            iteration += 1
            sleep(self.sleep_time)


def main(config, network, dir):
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


    yaml_file = open(config, 'r')
    config = yaml.load(yaml_file, Loader=yaml.Loader)

    return TransactionGenerator(config['frecuencia'], config['NumEntradasMin'],
        config['NumEntradasMax'], config['NumSalidasMin'], config['NumSalidasMax'],
        nodes=nodes, dir=dir, host='127.0.0.1', port=16000)


if __name__ == "__main__":

    # Leer los parametros
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-f', type=str, help='Archivo de Configuracion del Generador')
    parser.add_argument('-n', type=str, help='Archivo de red de Nodos')
    parser.add_argument('-d', type=str, help='Directorio del log del Nodo')
    args = parser.parse_args()
    
    generator = main(args.f, args.n, args.d)
    generator.start_generator()



