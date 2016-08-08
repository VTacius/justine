# coding: utf-8

from json import load, dump
from os import getcwd

class Usuarios:
   
    def __init__(self):
        self.direccion = getcwd()

    def listar(self):
        """
        Acá ocurrirá la más simple de todas las busquedas posibles: No más de 250 usuarios 
        """
        direccion = self.direccion + '/datos.d/usuarios_listado.json'
        fichero = open(direccion)
        contenido = load(fichero)
        return contenido[:250]

    def detalle(self, uid):
        """
        Acá obtenemos más detalles del usuario en base al rol del cliente
        TODO: Verificar rol del usuario
        """
        direccion = self.direccion + '/datos.d/usuarios_detalle_' + uid + '.json'
        try:
            fichero = open(direccion)
            contenido = load(fichero)
        except IOError as e:
            raise Exception()
        return contenido
        
       
if __name__ == '__main__':
    usuarios = Usuarios()
    usuarios.detalle('alortiz')
