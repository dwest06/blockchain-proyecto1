import names
import random
import gnupg

import hashlib
import base58


class Wallet(object):
    """
    Almacenamiento para private key de usuarios
    """

    gpg = gnupg.GPG()
    PASSPHRASE = "dg123456"
    TRANSACCION_NUEVA = 'transaccion_nueva'

    def __init__(self, name: str, lastname: str, email: str):
        self.name = name
        self.lastname = lastname
        self.email = email
        self.balance = 0

    # Identities
    def get_full_name(self) -> str:
        return f"{self.name} {self.lastname}"

    @classmethod
    def generate_random_person(cls):
        name = names.get_first_name()
        last = names.get_last_name()
        email = f"{name}-{last}{random.randint(0,999)}@testmail.com"
        return cls(name, last, email)

    def generate_keys(self):
        # https://gist.github.com/ryantuck/56c5aaa8f9124422ac964629f4c8deb0
        # Generate key
        input_data = self.gpg.gen_key_input(
            name_real = self.get_full_name(),
            name_email=self.email,
            passphrase=self.PASSPHRASE,
        )
        # Generate priv and pubkey
        key = self.gpg.gen_key(input_data)
        self.pubkey = self.gpg.export_keys(key.fingerprint)
        self.privkey = self.gpg.export_keys(key.fingerprint, True, passphrase=self.PASSPHRASE)
        
        # Generate address from pubkey
        pubhash = hashlib.sha1(self.pubkey.encode('utf-8'))
        # Generar el address iniciando con 0x10
        self.address = f"0x10{base58.b58encode(pubhash.hexdigest())}"

    # Tokens
    def set_balance(self, amount):
        if amount < 0:
            return "Amount must be positive"
        self.balance += amount


    def sign_data(self, data):
        # TODO: Firmar la data
        # Encriptar con la llave privada
        return data

    def emit_transaction(self, transaction):
        # Conectarse con algun nodo y enviar mensaje de nueva transaccion
        # Buscar un nodo
        nodo = self.nodes_network[random.randint(0, len(self.nodes_network))]
        # Contruir el mensaje
        mensaje = {"message": self.TRANSACCION_NUEVA, "transacion": transaction}
        # Firmar el mensaje
        data = self.sign_data(mensaje)
        # Enviarla
        nodo.send_data(data)
        pass

    def refresh_balance(self):
        # Buscar en la blockchain sobre nuevas transacciones que se hayan realizado a esta billetera
        pass

    def __rep__(self):
        return self.get_full_name()

