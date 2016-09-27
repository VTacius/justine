# coding: utf-8
# Esto es una petición a una base de datos

import logging
log = logging.getLogger('justine')

USERS = ['vtacius', 'alortiz', 'cpena', 'figaro']

# Esto es otra peticion a una base de datos
ROLES = {
            'vtacius': ['administrador', 'tecnicosuperior', 'tecnicoatencion'], 
            'alortiz': ['tecnicosuperior', 'tecnicoatencion'],
            'usuario': ['usuario'],
            'figaro': ['tecnicoatencion'],
            'cpena': ['tecnicoatencion']
        }

def groupfinder(uid, request):
    # Estoy casi seguro que este ocurre con cada petición que los clientes hagan, 
    # así que lo pensás bien respecto a como acceder a la base de datos
    # Mirá, se supone lo que querrás, pero al final no es la aplicación quién nos 
    # confirma información, sino que
    # nosotros nos lo confirmamos en cada petición que se haga 
    if uid in USERS:
        return ROLES.get(uid, [])

