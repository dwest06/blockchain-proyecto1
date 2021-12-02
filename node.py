import argparse
import json
import yaml
import socket
import time
import random
import hashlib
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
        # self.debug = True
        # Attributes
        self.blockchain = BlockChain()
        self.pool_transactions = []
        self.mining_proccess = True

        # Address, pubkey, privkey
        wallet = Wallet.generate_random_person()
        wallet.generate_keys()
        # Logger, Configs y Network
        self.logger = Logger(node_name, log_dir, True)
        self.config = config or NodeConfig()
        self.network_nodes = network_nodes

        # Connect to other nodes
        for node in network_nodes[node_name]['connections']:
            self.connect_with_node(network_nodes[node]['host'], int(network_nodes[node]['port']))

        print(f"Node {self.id}: Started")

    def get_transaction_list(self) -> list:
        """
        Metodo para agarrar lista de transacciones para generar el bloque
        """
        block_size = 0
        # Iniciar con el Coinbase 
        # TODO: Generar el Coinbase
        transaction_list = []
        # Obtener maximo de transacciones
        for i in self.pool_transactions:
            # TODO: poner el Transaccion el tamaño real de la transaccion
            block_size += 100
            if block_size > self.config.max_block_size:
                break
            transaction_list.append(i)

        return transaction_list

    def generate_block(self, transaction_list):
        """
        Generar un bloque con la lista de transacciones especificadas
        """
        return self.blockchain.generate_block(transaction_list)

    def mine(self, block):
        """
        Metodo de PoW
        """

        block_header = block.previous_block_hash + str(block.timestamp) + str(block.difficulty) + block.merkle_tree_root

        while True:
            # Flag para para el minado si otro nodo encontro el nonce
            if self.found_block:
                # Regresar las transacciones al pool
                pass
                # Revisar las transacciones que se minaron y eliminarlas

                break

            nonce = random.randint(0, block.NONCE_LIMIT)
            block_data =  block_header + str(nonce)
            hash_try = hashlib.sha256((block_data).encode()).hexdigest()
            if (hash_try.startswith(self.difficulty * '0')):
                block.nonce = nonce
                block.hash = hash_try
                break
        
        # Guardar el hash 
        if hash_try:
            self.hash = hash_try
            return True
        return False

    def start_minig_process(self):
        """
        Metodo principal donde se van a estar minando indefinidamente
        """
        print("Start Mining Proccess...")
        while True:

            # Flag para para el proceso de minado
            if not self.mining_proccess:
                self.mining_proccess = True
                break
            
            start = time.time()
            transaction_list = self.get_transaction_list() # Obtener lista de transacciones
            block = self.generate_block(transaction_list) # Genera el bloque
            result = self.mine(block) # Minar el Bloque
            print(f"Minado en {time() - start} seg")
            if result:
                self.blockchain.addBlock(block) # Agregar al blockchain
                self.propagate_candidate_block(None, block) # Propagar el Bloque

        print("Mining Stop")

    def exist_in_blockchain(self, block:Block) -> bool:
        # Return True if block exist in Node Blockchain
        return bool(self.blockchain.search_block_by_hash(block.hash))

    def exist_in_pool_tx(self, transaction: Transaction) -> bool:
        # Return True if transaction exist in Node Blockchain
        for tx in self.pool_transactions:
            if tx.hash == transaction.hash:
                return True
        return False

    # NODE MESSAGES
    def enter_transaction(self, nodo, transaction):

        # Create transaction object from dict
        # transaction = Transaction.from_dict(dict)

        # Validar la Transaccion, se pasa al blockchain que busque si 
        if not self.blockchain.validate_transaction(transaction):
            # Retornar ACK del mesaje
            data = json.dumps({"message": self.TRANSACCION_NUEVA_ACK, "estado": "NO"})
            self.send_to_node(node, data)
            return False
        
        # Agregar la transaccion al pool de transacciones
        self.pool_transactions.append(transaction)
        
        # Retransmitir
        data = json.dumps({"message": self.TRANSACCION_NUEVA, "data": transaction })
        self.send_to_nodes(data, exclude=[nodo])
        
        # Retornar ACK del mensaje
        data = json.dumps({"message": self.TRANSACCION_NUEVA_ACK, "estado": "SI"})
        self.send_to_node(nodo, data)

        return True

    def presentation(self, node):
        # Intercambiar claves publicas para establecer confianza
        # TODO: Agregar lista de pk de cada nodo conectado

        # Retornar ACK del mesaje
        data = json.dumps({"message": self.PRESENTACION_ACK, 'estado': 'SI'})
        self.send_to_node(node, data)

        return True

    def propagate_transaction(self, node, transaction):
        
        # Create transaction object from dict
        # transaction = Transaction.from_dict(transaction)

        # Validar la Transaccion, se pasa al blockchain que busque si 
        if not self.blockchain.validate_transaction(transaction):
            data = json.dumps({"message": self.PROPAGAR_TRANSACCION_ACK, "estado": "NO"})
            self.send_to_node(node, data)
            return False

        # Validar que no este en la pool de transacciones
        if self.exist_in_pool_tx(transaction) and node:
            # Retornar un ACK con estado SI ya que si se habia agregado
            data = json.dumps({"message": self.PROPAGAR_TRANSACCION_ACK, "estado": "SI"})
            self.send_to_node(node, data)
            return True

        # Agregar al pool de transacciones
        self.pool_transactions.append(transaction)

        # Propagar
        data = json.dumps({'message': self.PROPAGAR_TRANSACCION,'data': transaction.to_dict()})
        self.send_to_nodes(data, exclude=[node])

        # Retornar ACK del mesaje
        data = json.dumps({"message": self.PRESENTACION_ACK, 'estado': 'SI'})
        self.send_to_node(node, data)

        return True

    def propagate_candidate_block(self, node, block):
        # Create Block From Dict
        # block = Block.from_dict(block)

        # Validar que no este en la blockchain
        if self.exist_in_blockchain(block) and node:
            # Retornar un ACK con estado SI ya que si se habia agregado
            data = json.dumps({"message": self.PROPAGAR_BLOQUE_ACK, "estado": "SI"})
            self.send_to_node(node, data)
            return True

        # Validar bloque
        if not self.blockchain.verify_block(block, None, None, None):
            data = json.dumps({"message": self.PROPAGAR_BLOQUE_ACK, "estado": "NO"})
            self.send_to_node(node, data)
            return False

        # Propagar
        data = json.dumps({'message': self.PROPAGAR_BLOQUE, 'data': block.to_dict()})
        self.send_to_nodes(data, exclude=[node])

        # Retornar ACK del mesaje
        if node:
            data = json.dumps({"message": self.PROPAGAR_BLOQUE_ACK, "estado": "SI"})
            self.send_to_node(node, data)

        return True

    # P2P FUNCTIONALITIES

    def node_message(self, node, data):
        """
        Handler for communications between nodes
        """
        try:
            message = data['message']
            result = False

            # MAIN MESSAGES
            if message == self.TRANSACCION_NUEVA:
                print(f"{self.TRANSACCION_NUEVA} - {data['data']}")
                self.enter_transaction(node, data['data'])
            elif message == self.PRESENTACION:
                print(f"{self.PRESENTACION} - {data['data']}")
                result = self.presentation(node)
            elif message == self.PROPAGAR_TRANSACCION:
                print(f"{self.PROPAGAR_TRANSACCION} - {data['data']}")
                result = self.propagate_transaction(node, data['data'])
            elif message == self.PROPAGAR_BLOQUE:
                print(f"{self.PROPAGAR_BLOQUE} - {data['data']}")
                result = self.propagate_candidate_block(node, data['data'])

            # ACK
            elif message == self.TRANSACCION_NUEVA_ACK:
                print(f"{self.TRANSACCION_NUEVA_ACK} - {data['estado']}")
                self.logger.
                # result = self.enter_transaction(node, data['data'])
            elif message == self.PRESENTACION_ACK:
                print(f"{self.PRESENTACION_ACK} - {data['estado']}")
                # result = self.presentation(node)
            elif message == self.PROPAGAR_TRANSACCION_ACK:
                print(f"{self.PROPAGAR_TRANSACCION_ACK} - {data['estado']}")
                # result = self.propagate_transaction(data['data'])
            elif message == self.PROPAGAR_BLOQUE_ACK:
                print(f"{self.PROPAGAR_BLOQUE_ACK} - {data['estado']}")
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
            if name == n.id:
                return n
            
        return None

    def send_to_node(self, n, data):
        # Revisar que si es name (id) o el node como tal
        node = self.get_node_from_name(n) if isinstance(n, str) else n
        print(f"NODE NAME: {n} NODE SEARCH: {node}")
        return super().send_to_node(node, data)
    
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
    generator = Node(name, nodes[name]['host'], nodes[name]['port'], nodes, config=conf, log_dir=directory)

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

    # Start Socket Server
    node.start()

    # Start Mining proccess
    node.start_minig_process()



# p3 node.py -n nodo1 -d . -f archivo_red.txt -c node_config.yaml