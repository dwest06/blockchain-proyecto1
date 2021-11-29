from p2pnetwork.node import Node as Node_Socket

class Node(Node_Socket):

    def __init__(self, node_number: int, host, port, id=None, callback=None, max_connections=0):
        super().__init__(host, port, id, callback, max_connections)
        self.number = node_number
        self.blockchain = None
        self.pool_transactions = None
        self.adjacent_nodes = []

        self.init_node()

        print("MyPeer2PeerNode: Started")

    def mine(self, difficulty):
        # Encontrar un hash que cumpla con la dificultad
        pass

    
    def enter_transaction(self, remitente, transaction):
        # Validar la Transaccion
        if not transaction.valid():
            return {"message": "transaccion nueva", "remitente": remitente, "estado": "No"}

        # Agregar la transaccion al pool de transacciones

        # Retornar ACK del mensaje

        return {"message": "transaccion nueva", "remitente": remitente, "estado": "Si"}

    def presentation(self, new_node):
        # Identificar nodo

        # Agregar nuevo nodo a la lista de nodos adyacentes

        return {"message": "transaccion nueva", "remitente": new_node}


    def propagate_transaction(self):
        # Enviar la transaccion a los nodos adyacentes
        for i in self.adjacent_nodes:
            # Send transaccion
            pass

        return 

    def propagte_candidate_block(self, block):
        # Validar que no se ha verificado
        if block in self.blockchain:
            return 

        # Enviar bloque a los nodos adyacentes
        for i in self.adjacent_nodes:
            # Send node
            pass
        
        return

    # all the methods below are called when things happen in the network.
    # implement your network node behavior to create the required functionality.

    def outbound_node_connected(self, node):
        print("outbound_node_connected (" + self.id + "): " + node.id)
        
    def inbound_node_connected(self, node):
        print("inbound_node_connected: (" + self.id + "): " + node.id)

    def inbound_node_disconnected(self, node):
        print("inbound_node_disconnected: (" + self.id + "): " + node.id)

    def outbound_node_disconnected(self, node):
        print("outbound_node_disconnected: (" + self.id + "): " + node.id)

    def node_message(self, node, data):
        print("node_message (" + self.id + ") from " + node.id + ": " + str(data))
        
    def node_disconnect_with_outbound_node(self, node):
        print("node wants to disconnect with oher outbound node: (" + self.id + "): " + node.id)
        
    def node_request_to_stop(self):
        print("node is requested to stop (" + self.id + "): ")



    def __str__(self):
        return f"Node{self.number}"