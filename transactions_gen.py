import argparse
import socket
from time import sleep
from random import randint
from p2pnetwork.node import Node
import yaml
from transaction import Transaction
import random
import json
from transaction import Gasto

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

    def search_address(self, file):
        # Opening JSON file
        f = open(file)

        # returns JSON object as
        # a dictionary
        data = json.load(f)

        address_list = []

        # Iterating through the json
        for i in data:
            address_list.append(data[i]['address'])

        # Closing file
        f.close()

        return address_list

    def transacciones_no_gastadas(self, _from_address):
        list_utxo_from = []

        #TODO: Buscar las UTXO asociadas a _from_address y guardarlas en una lista

        return list_utxo_from

    def generate_transaction(self, num_salidas, _from, _to_list: list):
        # Generar la transaccion con la sintaxis de P2SH

        list_utxo = self.transacciones_no_gastadas(_from)

        # Check in range
        if self.ent_min <= len(list_utxo) <= self.ent_max:

            num_ent = random.randint(self.ent_min, len(list_utxo))
            
            acc = 0
            entradas = []
            gastos = []
            for i in range (num_ent):
                acc += list_utxo[i].amount
                entradas.append(list_utxo[i])
                list_utxo[i].detail = 'spend'

            # Generar amount
            amount_total = random(0, acc)

            # Monto a enviar
            amount_div = amount_total/num_salidas

            # No-change transaction
            if acc == amount_total:

                # TODO: _to debe ser lista de address de tamanio num_salidas
                for i in range (num_salidas):
                    gastos.append(Gasto(_to_list[i], amount_div))

                transaction = Transaction(entradas, gastos)

            # Transaction with change
            elif acc > amount_total:
                change = acc-amount_total

                # TODO: _to debe ser lista de address de tamanio num_salidas
                for i in range (num_salidas + 1):
                    if i != num_salidas:
                        gastos.append(Gasto(_to_list[i], amount_div, index=i))
                    else:
                        gastos.append(Gasto(_from, change, index=i))

                transaction = Transaction(entradas, gastos)
                
        else:
            transaction = Transaction(None, None)
            
        return transaction



    def send_transaction(self, transaction):
        # Get Random Node
        node_name = random.choice(list(self.nodes.keys()))
        node = self.node[node_name]
        # Convert transaction to dict
        tx_dict = transaction.to_dict()
        # Send transaction to node 

        self.connect_with_node(node['host'], node['port'])

        data = json.dumps({
            "message": "transaccion_nueva",
            "data": tx_dict
        })
        self.send_to_nodes(data)

    def start_generator(self):
        iteration = 0
        while True:
            # For test only max_iterations are valids
            if iteration >= self.max_iteration:
                break
            
            # send transactions
            for i in range(self.frecuencia):
                # Buscar address de in y addres de out en el directorio
                address_list = self.search_address('wallets.json')

                # Realizar salidas
                num_salidas = random.randint(self.sal_min, self.sal_max)

                addr_in = random.choice(address_list)
                addr_out_list = []
                i = 0
                while i < num_salidas:
                    addr_out = random.choice(address_list)

                    if (addr_out == addr_in):
                        pass
                    else:
                        addr_out_list.append(addr_out)
                        i += 1
                
                # Creo que no debe llevar amount para poder analizar las entradas y salidas y de ahi escoger el monto
                # amount = 1000
                # transaction = self.generate_transaction(addr_in, addr_out, amount)

                transaction = self.generate_transaction(num_salidas, addr_in, addr_out_list)

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



