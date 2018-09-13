# coding: utf-8

from json import load
from os import path

import logging
log = logging.getLogger('justine')

def cargar_credenciales():
    token = 'eyJyb2wiOiAiYWRtaW5pc3RyYWRvciIsICJkaXJlY2Npb24iOiAiYWxvcnRpeiJ9.3wR/qMGedccms7xFXN+GCbxlhbTknXGaBrtK3byOzJ0='
    cabecera = 'WWW-Authorization'
    return {cabecera: token}

def cargar_datos(ente):
    directorio = path.dirname(__file__)
    ruta = directorio.split('tests')[0] + 'tests/'

    archivo = ruta + 'datos.json'
    fichero = open(archivo, 'rb')
    contenido = load(fichero)

    return contenido[ente]
    
