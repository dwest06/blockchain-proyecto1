import argparse
import json
from p2pnetwork.node import Node as Node_Socket

from src.block import Block
from src.blockchain import BlockChain
from src.wallet import Wallet
from src.transaction import Transaction


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

    def __init__(self, node_number: int, host, port, callback=None, max_connections=0):
        super().__init__(host, port, node_number, callback, max_connections)
        # DEBUG TRUE
        self.debug = True
        # Attributes
        self.blockchain = BlockChain()
        self.pool_transactions = []
        # Address, pubkey, privkey
        wallet = Wallet.generate_random_person()
        wallet.generate_keys()
        # Logger
        self.logger = None
        print(f"Node{self.id}: Started")

    def mine(self):
        # Encontrar un hash que cumpla con la dificultad
        print("Minando...")
        pass

    def validate_in_blockchain(self, block:Block) -> bool:
        # Return True if block not exist in Node Blockchain
        if self.blockchain.search_block_by_hash(block.hash):
            return False
        return True

    # NODE MESSAGES

    def enter_transaction(self, nodo, transaction: Transaction):
        # Validar la Transaccion
        if not transaction.valid():
            return {"message": self.TRANSACCION_NUEVA_ACK, "estado": "NO"}

        # Agregar la transaccion al pool de transacciones
        self.pool_transactions.append(transaction)

        # Retornar ACK del mensaje
        return {"message": self.TRANSACCION_NUEVA_ACK, "estado": "SI"}

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
        self.send_to_nodes(data, exclude=self.nodes_inbound)
        return True

    # P2P FUNCTIONALITIES

    def node_message(self, node, data):

        print("node_message (" + self.id + ") from " + node.id + ": " + str(data))

        try:
            data = json.loads(data)
            message = data['message']
            result = False
            if message == self.TRANSACCION_NUEVA:
                result = self.enter_transaction(node, data['data'])
            elif message == self.PRESENTACION:
                result = self.presentation(node)
            elif message == self.PROPAGAR_TRANSACCION:
                result = self.propagate_transaction(data['data'])
            elif message == self.PROPAGAR_BLOQUE:
                result = self.propagate_candidate_block(data['data'])
            
            # Retornar el ACK del mensaje

            return response_to_node()

        except KeyError:
            # Retornar al nodo emisor el tipo de fallo
            pass
        except Exception as e:
            # Reportar cualquier otro fallo/ Reportar error de loads del json
            pass

        
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



if __name__ == "__main__":

    # Leer los parametros
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-n', type=str, help='Nombre del Nodo')
    parser.add_argument('-d', type=str, help='Directorio del archivo de .log')
    parser.add_argument('-f', type=str, help='Archivo de Configuracion de la Red')
    parser.add_argument('-c', type=str, help='Archivo de Configuracion')
    args = parser.parse_args()

    # Procesar parametros, 
    
    generator = Node()