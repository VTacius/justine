# coding: utf-8

import datetime
# Las siguientes librerías son parte del core actual, podrían volverse innecesarias cuando use la
# API de Samba4
from json import load, dump
from os import getcwd, remove, listdir

# No tendría sentido que manejemos logggin desde tan abajo de la aplicación, que no sea en desarrollo
import logging
log = logging.getLogger('justine')

class Computadoras:
   
    def __init__(self):
        self.direccion = getcwd()
    
    def listar(self):
        """
        Acá ocurrirá la más simple de todas las busquedas posibles: No más de 250 computadoras 
        """
        pass
