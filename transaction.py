"""
BITCOIN RAW TRANSACTION
{
  "version": 1,
  "locktime": 0,
  "vin": [
    {
      "txid": "7957a35fe64f80d234d76d83a2a8f1a0d8149a41d81de548f0a65a8a999f6f18",
      "vout": 0,
      "scriptSig" : "3045022100884d142d86652a3f47ba4746ec719bbfbd040a570b1deccbb6498c75c4ae24cb02204b9f039ff08df09cbe9f6addac960298cad530a863ea8f53982c09db8f6e3813[ALL] 0484ecc0d46f1918b30928fa0e4ed99f16a0fb4fde0735e7ade8416ab9fe423cc5412336376789d172787ec3457eee41c04f4938de5cc17b4a10fa336a8d752adf",
      "sequence": 4294967295
    }
  ],
  "vout": [
    {
      "value": 0.01500000,
      "scriptPubKey": "OP_DUP OP_HASH160 ab68025513c3dbd2f7b92a94e0581f5d50f654e7 OP_EQUALVERIFY OP_CHECKSIG"
    },
    {
      "value": 0.08450000,
      "scriptPubKey": "OP_DUP OP_HASH160 7f9b1a7fb68d60c536c2fd8aeaa53a8f3cc025a8 OP_EQUALVERIFY OP_CHECKSIG",
    }
  ]
}
"""
import hashlib
import json
from functools import reduce
from time import time

class Entrada(object):
    """
    Clase para representar los VIN(Entrada)
    """

    def __init__(self, tx_hash_ref, index, sender, amount, detail="unspend") -> None:
        self.tx_hash_ref = tx_hash_ref # Hash de la transaccion donde esta el UTXO
        self.index = index # Index del UTXO que refiere a esta entrada dentro de la transaccion confirmada
        self.sender = sender # Address del que envia el valor
        self.amount = amount # Valor que se envia
        # self.sigscript = None 
        # self.pkscript = None
        self.detail = detail # Puede ser 'unspend' o 'spend'
        

    def to_dict(self):
        return {
          "tx_hash_ref": self.tx_hash_ref,
          "index": self.index,
          "sender": self.sender,
          "amount": self.amount,
          "detail": self.detail
        }

    @classmethod
    def from_dict(cls, dict):
        return cls(dict['tx_hash_ref'], dict['index'], dict['sender'], dict['amount'], dict['detail'])


class Gasto(object):
    """
    Clase para representar los VOUT(Gastos)
    """

    def __init__(self, reciever, amount, detail="unspend", index=0) -> None:
        self.reciever = reciever
        self.amount = amount
        # self.sigscript = None 
        # self.pkscript = None
        self.detail = detail
        self.index = index

    def to_dict(self):
      return {
        "reciever": self.reciever,
        "amount": self.amount,
        "detail": self.detail,
        "index": self.index
      }

    @classmethod
    def from_dict(cls, dict):
      return cls(dict['reciever'], dict['amount'], dict['detail'], dict['index'])


class Transaction(object):
    """
    Clase para representar la transaccion
    """

    def __init__(self, entradas: list, gastos: list, coinbase = False):
        self.timestamp = time() # Tiempo cuando fue creado
        self.entradas = entradas # Lista de las Entradas de la transaccion
        self.gastos = gastos # lista de Gastos de la transaccion
        self.estado = False # Estado, True para confirmada, False de lo contrario
        self.block_index = None # Indice del bloque donde fue incluida la transaccion
        self.entradas_totales = self.calculate_total(self.entradas)
        self.gastos_totales = self.calculate_total(self.gastos)
        self.hash = self.calculate_hash()
        self.coinbase = coinbase # Flag para saber si es una entrada de coinbase
        self.size = self.calculate_size()

    def calculate_total(self, lista):
        acc = 0
        for i in lista:
            acc += i.amount
        return acc
      

    def calculate_hash(self):
        # Se calcula con el timestamp + block_index + entradas + gastos 
        # Hay que pasar todo a string, concatenar y calcular el hash
        text = ''
        for entrada in self.entradas:
            text += json.dumps(entrada.to_dict())
        for gasto in self.gastos:
            text += json.dumps(gasto.to_dict())
        hash = hashlib.sha256((str(self.timestamp) + str(self.block_index) + text).encode('utf-8'))
        return hash.hexdigest()

    def calculate_size(self):
        """
        Method to calculate size, convert self to dict, after in str
        """
        return len(json.dumps(self.to_dict()))
            
    def validate_amounts(self):
        # Validar que hay entradas y gastos
        if not len(self.entradas) or not len(self.gastos):
            return False

        # Verificar que amount de entradas > gastos
        total = 0
        for i in self.entradas:
            total += i.amount
        for i in self.gastos:
            total -= i.amount
        # NOTE: Como no se esta cobrando comision, es valido que sea igual a 0
        # En caso de cobrar comision tiene que se estrictamente mayor a 0
        if total < 0:
            return False

        return True

    @classmethod
    def generate_coinabse(cls, address):
        entrada = Entrada(None, None, 50, 0)
        gasto = Gasto(address, 50)
        return cls([entrada], [gasto], coinbase=True)

    def to_dict(self):
      return {
        "timestamp": self.timestamp,
        "entradas": [ entrada.to_dict() for entrada in self.entradas],
        "gastos": [ gasto.to_dict() for gasto in self.gastos],
        "estado": self.estado,
        "block_index": self.block_index, 
        "entradas_totales": self.entradas_totales,
        "gastos_totales": self.gastos_totales,
        "hash": self.hash,
        "coinbase": self.coinbase
      }

    @classmethod
    def from_dict(cls, dict):
      entradas = [Entrada.from_dict(entrada) for entrada in dict['entradas'] ]
      gastos = [Gasto.from_dict(gasto) for gasto in dict['gastos'] ]
      tx = cls(entradas, gastos)
      tx.timestamp = dict['timestamp']
      tx.estado = dict['estado']
      tx.block_index = dict['block_index']
      tx.entradas_totales = dict['entradas_totales']
      tx.gastos_totales = dict['gastos_totales']
      tx.hash = dict['hash']
      tx.coinbase = dict['coinbase']
      return tx
