# coding: utf-8

import datetime
# Las siguientes librerías son parte del core actual, podrían volverse innecesarias cuando use la
# API de Samba4
from json import load, dump
from os import getcwd, remove

# No tendría sentido que manejemos logggin desde tan abajo de la aplicación, que no sea en desarrollo
import logging
log = logging.getLogger('justine')

class Establecimientos:
   
    def __init__(self):
        self.direccion = getcwd()
    
    def listar(self):
        """
        Acá ocurrirá la más simple de todas las busquedas posibles: No más de 250 usuarios 
        """
        try:
            direccion = self.direccion + '/datos.d/helpers_establecimientos.json'
            fichero = open(direccion)
            contenido = load(fichero)
        except IOError as e:
            raise IOError
        return contenido

class Oficinas:
    
    def __init__(self):
        self.direccion = getcwd()

    def listar(self, establecimiento):
        """
        Acá ocurrirá la más simple de todas las busquedas posibles: No más de 250 usuarios 
        """
        direccion = self.direccion + '/datos.d/helpers_oficinas.d/' + establecimiento + '.json'
        fichero = open(direccion)
        contenido = load(fichero)
        return contenido

