# coding: utf-8

from pyramid.view import view_config
from pyramid import httpexceptions as exception  

from ..juliette.grupos import Grupos

from cerberus import ValidationError

import logging
log = logging.getLogger('justine')

@view_config(route_name='grupos_listado', renderer='json', permission='listar')
def grupos_listado(peticion):
    grupos = Grupos()
    contenido =  grupos.listar()[:150]
    return contenido

@view_config(route_name='grupos_detalle', renderer='json')
def grupos_detalle (peticion):

    # Validando datos recibidos
    try:
        gidNumber = peticion.matchdict['grupo'] 
    except KeyError as e:
        log.error(e)
        return exception.HTTPBadRequest(headers=(('Access-Control-Allow-Origin', '*'),))
    
    grupos = Grupos()
   
    # Realizamos la operación Detalle de Grupos mediante la librería 
    try: 
        contenido = grupos.detalle(gidNumber)
    except IOError as e:
        log.error(e)
        return exception.HTTPNotFound(headers=(('Access-Control-Allow-Origin', '*'),))
    except Exception as e:
        log.error(e)
        return exception.HTTPInternalServerError(headers=(('Access-Control-Allow-Origin', '*'),))
    
    return {'mensaje': contenido}
    
