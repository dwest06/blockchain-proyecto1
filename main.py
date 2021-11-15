from subprocess import call
from yaml import load, Loader
import yaml


def set_configs(archivo_config: str, archivo_nodo: str, dir: str):
    yaml_file = open(archivo_config, 'r')
    config = load(yaml_file, Loader=Loader)


def get_command(command: str):

    c = command.split(' ')
    name = None
    if c[0] == 'initnode':
        if c[1] == '-n':
            name = c[2]
            print(f"Llamando para iniciar Nodo {name}")
            call(['gnome-terminal', '-e', f"python3 ./test.py {name}"])
        
    if c[0] == 'network':
        # from pprint import pprint
        with open('archivo_red.txt', 'r') as red:
            print("Red Virtual de Nodos")
            print(red.read())


if __name__ == "__main__":
    while True:
        command = input(">>>>>>>> ")
        # end loop
        if command == 'end':
            break

        proccess_command = get_command(command)
