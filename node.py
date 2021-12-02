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

    def __init__(self, max_block_size = 512, creation_block_average_time = 1, initial_difficulty = 5) -> None:
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

    def __init__(self, node_name, host, port, network_nodes, callback=None,
        max_connections=0, log_dir = '.', config = None, init=False):

        super().__init__(host, int(port), node_name, callback, max_connections)
        # self.debug = True
        # Address, pubkey, privkey
        self.wallet = Wallet.generate_random_person()
        self.wallet.generate_keys()

        # Logger, Configs y Network
        self.logger = Logger(node_name, log_dir, True)
        self.config = config or NodeConfig()
        self.network_nodes = network_nodes

        # Attributes
        self.blockchain = BlockChain()

        self.pool_transactions = []
        self.mining_proccess = True
        self.found_block = False

        # Connect to other nodes
        for node in network_nodes[node_name]['connections']:
            self.connect_with_node(network_nodes[node]['host'], int(network_nodes[node]['port']))

        print(f"Node {self.id}: Started")

        if init:
            # Generar el Genesis Block
            start = time.time()
            genesis = self.blockchain.create_genesis_block(self.wallet.address)
            self.blockchain.addBlock(genesis)
            self.logger.info(f"Minado Bloque Genesis en {time.time() - start} seg")

        else:
            # Presentarse con los otros nodos, elegir un nodo para recopilar la data de la blockchain
            pass

    def get_transaction_list(self) -> list:
        """
        Metodo para agarrar lista de transacciones para generar el bloque
        """
        block_size = 0
        coinbase = self.blockchain.generate_coinbase(self.wallet.address)
        transaction_list = [coinbase]

        # Obtener maximo de transacciones
        for tx in self.pool_transactions:
            block_size += tx.size
            if block_size > self.config.max_block_size:
                break
            transaction_list.append(tx)

        # Quitar las transacciones del pool
        self.pool_transactions = self.pool_transactions[len(transaction_list):]

        return transaction_list

    def generate_block(self, transaction_list):
        """
        Generar un bloque con la lista de transacciones especificadas
        """
        return self.blockchain.generate_block(transaction_list)

    def change_transaction_status(self, block):
        return self.blockchain.change_transaction_status(block)


    def mine(self, block):
        """
        Metodo de PoW
        """
        block_header = block.previous_block_hash + str(block.timestamp) + str(block.difficulty) + block.merkle_tree_root

        while True:
            # Flag para para el minado si otro nodo encontro el nonce
            if self.found_block:
                # TODO: Hacer el RollBack si ya se mino un bloque
                # Regresar las transacciones al pool
                self.found_block = False # Resetear el flag
                # Revisar las transacciones que se minaron y eliminarlas
                break

            nonce = random.randint(0, block.NONCE_LIMIT)
            block_data =  block_header + str(nonce)
            hash_try = hashlib.sha256((block_data).encode()).hexdigest()
            if (hash_try.startswith(block.difficulty * '0')):
                block.nonce = nonce
                block.hash = hash_try
                self.change_transaction_status(block)
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
            if result:
                index = self.blockchain.addBlock(block) # Agregar al blockchain
                self.logger.info(f"Minado Bloque {index} en {time.time() - start} seg")
                self.propagate_own_block(block.to_dict()) # Propagar el Bloque

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
        transaction = Transaction.from_dict(transaction)

        # Validar la Transaccion, se pasa al blockchain que busque si 
        if not self.blockchain.validate_transaction(transaction):
            # Retornar ACK del mesaje
            data = json.dumps({"message": self.TRANSACCION_NUEVA_ACK, "estado": "NO"})
            self.send_to_node(node, data)
            return False
        
        # Agregar la transaccion al pool de transacciones
        self.pool_transactions.append(transaction)
        
        # Retransmitir
        data = json.dumps({"message": self.TRANSACCION_NUEVA, "data": transaction.to_dict() })
        self.send_to_nodes(data, exclude=[nodo])
        
        # Retornar ACK del mensaje
        data = json.dumps({"message": self.TRANSACCION_NUEVA_ACK, "estado": "SI"})
        self.send_to_node(nodo, data)

        return True

    def presentation(self, node):
        # Intercambiar claves publicas para establecer confianza
        # TODO: Agregar lista de pk de cada nodo conectado


        # TODO: Retornar la blockchain y transaction pool al nuevo nodo

        # Retornar ACK del mesaje
        data = json.dumps({"message": self.PRESENTACION_ACK, 'estado': 'SI'})
        self.send_to_node(node, data)

        return True

    def propagate_transaction(self, node, transaction):
        
        # Create transaction object from dict
        transaction = Transaction.from_dict(transaction)

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

    def propagate_own_block(self, block):
        # Propagar
        data = json.dumps({'message': self.PROPAGAR_BLOQUE, 'data': block})
        self.send_to_nodes(data, exclude=[node])

    def propagate_candidate_block(self, node, block):
        # Create Block From Dict
        block = Block.from_dict(block)

        # Validar que no este en la blockchain
        if self.exist_in_blockchain(block):
            # Retornar un ACK con estado SI ya que si se habia agregado
            data = json.dumps({"message": self.PROPAGAR_BLOQUE_ACK, "estado": "SI"})
            if node:
                self.send_to_node(node, data)
            return True

        # Validar bloque
        if not self.blockchain.verify_block(block):
            data = json.dumps({"message": self.PROPAGAR_BLOQUE_ACK, "estado": "NO"})
            self.send_to_node(node, data)
            return False

        # Parar el proceso de minado
        self.found_block = True

        # Agregar bloque al Blockchain
        self.blockchain.addBlock(block)

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
        print(f"MENSAJE RECIBIDO: {data}")
        try:
            message = data['message']
            result = False

            # MAIN MESSAGES
            if message == self.TRANSACCION_NUEVA:
                result = self.enter_transaction(node, data['data'])
                if result:
                    self.logger.info(f"Transaccion Nueva propagada")
                else:
                    self.logger.error(f"Transaccion Nueva No se pudo propagar")
                # print(f"{self.TRANSACCION_NUEVA} - {data['data']}")
            elif message == self.PRESENTACION:
                result = self.presentation(node)
                if result:
                    self.logger.info(f"Presentacion Exitosa")
                else:
                    self.logger.error(f"Presentacion No Exitosa")
            elif message == self.PROPAGAR_TRANSACCION:
                result = self.propagate_transaction(node, data['data'])
                if result:
                    self.logger.info(f"Propagar Transaccion Exitosa")
                else:
                    self.logger.error(f"Propagar Transaccion No Exitosa")
            elif message == self.PROPAGAR_BLOQUE:
                result = self.propagate_candidate_block(node, data['data'])
                if result:
                    self.logger.info(f"Propagar Bloque Exitosa")
                else:
                    self.logger.error(f"Propagar Bloque No Exitosa")

            # ACK
            elif message == self.TRANSACCION_NUEVA_ACK:
                self.logger.info(f"Transaccion Nueva ACK recieved with Status: {data['estado']}")
            elif message == self.PRESENTACION_ACK:
                self.logger.info(f"Presentacion ACK recieved with Status: {data['estado']}")
            elif message == self.PROPAGAR_TRANSACCION_ACK:
                self.logger.info(f"Propagar Transaccion ACK recieved with Status: {data['estado']}")
            elif message == self.PROPAGAR_BLOQUE_ACK:
                self.logger.info(f"Propagar Bloque ACK recieved with Status: {data['estado']}")


            elif message == 'block_explorer_a':
                block = self.blockchain.search_block_by_index(int(data['data']))
                self.send_to_node(node, json.dumps({'explorer': True, "data": block.to_dict()}))

            elif message == 'block_explorer_h':
                block = self.blockchain.search_block_by_index(int(data['data']))
                self.send_to_node(node, json.dumps({'explorer': True, "data": block.to_dict()}))

            elif message == 'transac_explorer':
                tx = self.blockchain.search_tx_by_hash(data['data'])
                self.send_to_node(node, json.dumps({'explorer': True, "data": tx.to_dict()}))

        except KeyError as e: # Retornar al nodo emisor el tipo de fallo
            self.logger.error(f"KEY ERROR: {e}")
        except Exception as e: # Reportar cualquier otro fallo/ Reportar error de loads del json
            self.logger.error(f"ERROR: {e}")
    

    def get_node_from_name(self, name):
        # Get NodeConnection by name
        for n in self.nodes_outbound:
            if name == n.id:
                return n
            
        return None

    def send_to_node(self, n, data):
        # Revisar que si es name (id) o el node como tal
        node = self.get_node_from_name(n) if isinstance(n, str) else n
        return super().send_to_node(node, data)
        
    def node_request_to_stop(self):
        self.logger.info(f"Node {self.id} is requested to STOP")


    # FOR LOGGING

    def outbound_node_connected(self, node):
        self.logger.info(f"Node {self.id} connected with {node.id}")
        
    def inbound_node_connected(self, node):
        self.logger.info(f"Node {node.id} connected with {self.id}")

    def inbound_node_disconnected(self, node):
        self.logger.info(f"Node {node.id} disconnected with {self.id}")

    def outbound_node_disconnected(self, node):
        self.logger.info(f"Node {self.id} disconnected with {node.id}")

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
    generator = Node(name, nodes[name]['host'], nodes[name]['port'], nodes, config=conf, log_dir=directory, init=True)

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