import names
import random
import gnupg
import datetime

from yaml import load, Loader
import yaml

gpg = gnupg.GPG()
PASSPHRASE = "dg123456"

class Logger():

    def __init__(self, dir:str = None):
        self.dir = dir
        self.logs = []

    def set_dir(self, new_dir):
        self.dir = new_dir

    def log(self, message:str):
        log = f"[LOG {datetime.datetime.now()}] - {message}"
        self.logs.append(log)

    def error(self, message:str):
        log = f"[ERROR {datetime.datetime.now()}] - {message}"
        self.logs.append(log)

    def dump_logs(self):
        # Verification dir
        if self.dir is None:
            raise Exception("Dir is None, set directory to dump logs")
        
        logs_file = open(f"logs-{datetime.datetime.now()}.txt", 'w+')

        for log in self.logs:
            logs_file.write(log)

        logs_file.close()


class Person():

    def __init__(self, name: str, lastname: str, email: str):
        self.name = name
        self.lastname = lastname
        self.email = email

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
        input_data = gpg.gen_key_input(
            name_real = self.get_full_name(),
            name_email=self.email,
            passphrase=PASSPHRASE,
        )
        key = gpg.gen_key(input_data)
        self.pk = gpg.export_keys(key.fingerprint)
        self.sk = gpg.export_keys(key.fingerprint, True, passphrase=PASSPHRASE)

    def __str__(self):
        return self.get_full_name()


class Node():

    def __init__(self, node_number: int):
        self.number = node_number

    def __str__(self):
        return f"Node{self.number}"


class Identities():
    
    def __init__(self):
        self.num_identities = 0
        self.num_nodes = 0

    @classmethod
    def generate_indetities(cls, num_identities: int, num_nodes: int):
        identities = cls()
        identities.num_identities = num_identities
        identities.num_nodes = num_nodes

        # Dict for storing identities
        indentities = {}
        for i in range(num_identities):
            # Generar identidades random
            person = Person.generate_random_person()

            # Crear claves
            person.generate_keys()

            # Save person
            identities[person.email] = person

        # Nodes
        for i in range(num_nodes):
            pass



def set_configs(archivo_config: str, archivo_nodo: str, dir: str):
    yaml_file = open(archivo_config, 'r')
    config = load(yaml_file, Loader=Loader)



if __name__ == "__main__":
    pass