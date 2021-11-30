import argparse
from time import sleep
from random import randint

class TransactionGenerator(object):

    sleep_time = 60
    max_iterations = 10

    def __init__(self, frecuencia, ent_min, ent_max, sal_min, sal_max, nodos, dir) -> None:
        # Configs
        self.frecuencia = frecuencia
        self.ent_min = ent_min
        self.ent_max = ent_max
        self.sal_min = sal_min
        self.sal_max = sal_max
        # States Node
        self.nodos = self.set_nodes(nodos)
        self.dir = dir

    def set_nodes(self, nodes_file):
        # Read Network file
        with open(nodes_file, 'r') as lines:
            n_nodes = lines.readline().rstrip()
            nodes = []
            for _ in range(int(n_nodes)):
                nodes.append(lines.readline().rstrip().split(' '))
            return nodes

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


if __name__ == "__main__":

    # Leer los parametros
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-f', type=str, help='Archivo de Configuracion del Generador')
    parser.add_argument('-n', type=str, help='Archivo de red de Nodos')
    parser.add_argument('-d', type=str, help='Directorio del log del Nodo')
    args = parser.parse_args()
    # access to arguments
    # print(args.f, args.n, args.d)
    generator = TransactionGenerator(args.f, args.n, args.d)



