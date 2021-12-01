import argparse
import json
import yaml
import socket
from p2pnetwork.node import Node as Node_Socket

from block import Block
from blockchain import BlockChain
from wallet import Wallet
from transaction import Transaction
from logger import Logger

class NodeConfig(object):

    def __init__(self, max_block_size = 512, creation_block_average_time = 1, initial_difficulty = 4) -> None:
        self.max_block_size = max_block_size
        self.creation_block_average_time = creation_block_average_time
        self.initial_difficulty = initial_difficulty

class Node(Node_Socket):

    # Mensajes
    TRANSACCION_NUEVA = 'transaccion_nueva'
    PRESENTACION = 'presentacion'
    PROPAGAR_TRANSACCION = 'transaccion'
    PROPAGAR_BLOQUE = 'bloque'
    # Mensajes ACK
    TRANSACCION_NUEVA_ACK = 'transaccion_nueva_ack'
    PRESENTACION_ACK = 'presentacion_ack'
    PROPAGAR_TRANSACCION_ACK = 'transaccion_ack'
    PROPAGAR_BLOQUE_ACK = 'bloque_ack'

    def __init__(self, node_name, host, port, network_nodes, callback=None, max_connections=0, log_dir = '.', config = None):
        super().__init__(host, int(port), node_name, callback, max_connections)
        # DEBUG TRUE
        self.debug = True
        # Attributes
        self.blockchain = BlockChain()
        self.pool_transactions = []
        # Address, pubkey, privkey
        wallet = Wallet.generate_random_person()
        wallet.generate_keys()
        # Logger
        self.logger = Logger(log_dir)
        # Config
        self.config = config or NodeConfig()

        # Network
        self.network_nodes = network_nodes

        # Connect to other nodes
        for node in network_nodes[node_name]['connections']:
            self.connect_with_node(network_nodes[node]['host'], int(network_nodes[node]['port']))
            print("Connecting ")

        print(f"Node {self.id}: Started")

    def mine(self):
        # Encontrar un hash que cumpla con la dificultad
        print("Minando...")
        pass

    def validate_in_blockchain(self, block:Block) -> bool:
        # Return True if block not exist in Node Blockchain
        return not bool(self.blockchain.search_block_by_hash(block.hash))


    # NODE MESSAGES
    def enter_transaction(self, nodo, transaction):
        # Validar la Transaccion
        # TODO: la transaccion llega como un json
        # if not transaction.valid():
        #     return {"message": self.TRANSACCION_NUEVA_ACK, "estado": "NO"}
        
        # Agregar la transaccion al pool de transacciones
        self.pool_transactions.append(transaction)
        # Retornar ACK del mensaje
        data = json.dumps({"message": self.TRANSACCION_NUEVA_ACK, "estado": "SI"})
        self.send_to_node(nodo, data)
        # Retransmitir
        data = json.dumps({"message": self.TRANSACCION_NUEVA, "data": transaction.to_dict() })
        self.send_to_nodes(data, exclude=[nodo])

    def presentation(self, node):
        # Identificar nodo
        
        # Agregar nuevo nodo a la lista de inbound_nodes
        self.nodes_inbound.append(node)
        # Retornar ACK del mesaje
        return {"message": self.PRESENTACION_ACK}


    def propagate_transaction(self, transaccion):
        data = {
            'message': self.PROPAGAR_TRANSACCION,
            'data': transaccion
        }
        # Enviar la transaccion a los nodos adyacentes
        self.send_to_nodes(data, exclude=self.nodes_inbound)
        return True

    def propagate_candidate_block(self, block):
        # Validar que no se ha verificado
        if self.validate_in_blockchain(block):
            return 

        data = {
            'message': self.PROPAGAR_BLOQUE,
            'data': block
        }

        # Enviar bloque a los nodos adyacentes
        self.send_to_nodes(data)
        return True

    # P2P FUNCTIONALITIES

    def node_message(self, node, data):

        print("node_message (" + self.id + ") from " + node.id + ": " + str(data))

        try:
            message = data['message']
            result = False
            
            # MAIN MESSAGES
            if message == self.TRANSACCION_NUEVA:
                print(f"{self.TRANSACCION_NUEVA} - {data}")
                self.enter_transaction(node, data['data'])
            elif message == self.PRESENTACION:
                print(f"{self.PRESENTACION} - {data}")
                # result = self.presentation(node)
            elif message == self.PROPAGAR_TRANSACCION:
                print(f"{self.PROPAGAR_TRANSACCION} - {data}")
                # result = self.propagate_transaction(data['data'])
            elif message == self.PROPAGAR_BLOQUE:
                print(f"{self.PROPAGAR_BLOQUE} - {data}")
                # result = self.propagate_candidate_block(data['data'])

            # ACK
            elif message == self.TRANSACCION_NUEVA_ACK:
                print(f"{self.TRANSACCION_NUEVA_ACK} - {data}")
                # result = self.enter_transaction(node, data['data'])
            elif message == self.PRESENTACION_ACK:
                print(f"{self.PRESENTACION_ACK} - {data}")
                # result = self.presentation(node)
            elif message == self.PROPAGAR_TRANSACCION_ACK:
                print(f"{self.PROPAGAR_TRANSACCION_ACK} - {data}")
                # result = self.propagate_transaction(data['data'])
            elif message == self.PROPAGAR_BLOQUE_ACK:
                print(f"{self.PROPAGAR_BLOQUE_ACK} - {data}")
                # result = self.propagate_candidate_block(data['data'])


        except KeyError:
            # Retornar al nodo emisor el tipo de fallo
            print("ERROR")
        except Exception as e:
            # Reportar cualquier otro fallo/ Reportar error de loads del json
            print("ERROR", e)
    

    def get_node_from_name(self, name):
        # Get NodeConnection by name
        for n in self.nodes_outbound:
            print(n)
            print(f"ID: {n.id}")
            if name == n.id:
                return n
            
        return None

    def send_to_node(self, n, data):
        # Revisar que si es name (id) o el node como tal
        node = n
        if isinstance(n, str):
            print(f"NODE NAME: {n}")
            node = self.get_node_from_name(n)

        return super().send_to_node(n, data)
    
    def node_disconnect_with_outbound_node(self, node):
        print("node wants to disconnect with oher outbound node: (" + self.id + "): " + node.id)
        
    def node_request_to_stop(self):
        print("node is requested to stop (" + self.id + "): ")


    # FOR LOGGING

    def outbound_node_connected(self, node):
        print("outbound_node_connected (" + self.id + "): " + node.id)
        
    def inbound_node_connected(self, node):
        print("inbound_node_connected: (" + self.id + "): " + node.id)

    def inbound_node_disconnected(self, node):
        print("inbound_node_disconnected: (" + self.id + "): " + node.id)

    def outbound_node_disconnected(self, node):
        print("outbound_node_disconnected: (" + self.id + "): " + node.id)

    def __str__(self):
        return f"Node{self.number}"


def main(name, directory, network, config_node):
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


    yaml_file = open(config_node, 'r')
    config = yaml.load(yaml_file, Loader=yaml.Loader)

    print(f"Generando {name} - {nodes[name]['host']}:{nodes[name]['port']}")
    print(f"conexiones {nodes[name]}")
    conf = NodeConfig(config['TamanioMaxBloque'], config['TiempoPromedioCreacionbloque'], config['DificultadInicial'])
    generator = Node(name, nodes[name]['host'], nodes[name]['port'], nodes, config=conf)

    return generator


if __name__ == "__main__":

    # Leer los parametros
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-n', type=str, help='Nombre del Nodo')
    parser.add_argument('-d', type=str, help='Directorio del archivo de .log')
    parser.add_argument('-f', type=str, help='Archivo de Configuracion de la Red')
    parser.add_argument('-c', type=str, help='Archivo de Configuracion')
    args = parser.parse_args()

    # Procesar parametros, 
    node = main(args.n, args.d, args.f, args.c)

    node.start()



# p3 node.py -n nodo1 -d . -f archivo_red.txt -c node_config.yaml