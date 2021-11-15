import sys
from time import sleep

if len(sys.argv) > 2:
    print(f"Iniciando Nodo {sys.argv[1]}")
else:
    print(f"Iniciando Nodo")

print("NAME: ", __name__)
sleep(2)
print("En proceso")
sleep(2)
print("Nodo iniciado exitosamente")
sleep(5)

def test():
    print("testing")

if __name__ == "__main__":
    print("MAIN TEST")