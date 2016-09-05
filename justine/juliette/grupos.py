# coding: utf-8

import datetime
# Las siguientes librerías son parte del core actual, podrían volverse innecesarias cuando use la
# API de Samba4
from json import load, dump
from os import getcwd, remove

# No tendría sentido que manejemos logggin desde tan abajo de la aplicación, que no sea en desarrollo
import logging
log = logging.getLogger('justine')

class Grupos:
   
    def __init__(self):
        self.direccion = getcwd()
    
    def listar(self):
        """
        Acá ocurrirá la más simple de todas las busquedas posibles: No más de 250 usuarios 
        """
        direccion = self.direccion + '/datos.d/grupos_listado.json'
        fichero = open(direccion)
        contenido = load(fichero)
        return contenido[:250]
    
    def detalle(self, gidNumber):
        """
        Acá obtenemos más detalles del grupo por medio del gidNumber en base al rol del cliente
        TODO: Verificar rol del usuario
        """
        # TODO: Mantengo este error porque necesito aprender a manejarlo en el cliente web
        direccion = self.direccion + '/datos.d/grupos_detalle_' + gidNumber + '.json'

        # Verifica que el grupo existe
        try:
            fichero = open(direccion)
            contenido = load(fichero)
        except IOError as e:
            raise IOError
        except Exception as e:
            raise Exception(e.args)

        return contenido
