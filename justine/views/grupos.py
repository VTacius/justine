# coding: utf-8

from pyramid.view import view_config
from pyramid import httpexceptions as exception  

from ..juliette.modelGroup import Grupo
from ..juliette.excepciones import DatosException, ConflictoException

#from ..schemas.grupos import EsquemaGrupo

import logging
log = logging.getLogger(__name__)

@view_config(route_name='grupos_listado', renderer='json', permission='listar')
def grupos_listado(peticion):
    try:
        grupo = Grupo()
        contenido = grupo.obtener()
    except Exception as e:
        log.error(e)
        return exception.HTTPInternalServerError()
    print contenido
    return contenido

@view_config(route_name='grupos_listado_options', renderer='json')
def grupos_listado_options(peticion):
    pass

@view_config(route_name='grupos_detalle', renderer='json')
def grupos_detalle (peticion):
    
    try:
        uid = peticion.matchdict['grupo'] 
    except KeyError as e:
        return exception.HTTPBadRequest()
    
    # Realizamos la operación Detalle de Usuarios mediante la librería
    try:
        grupo = Grupo()
        contenido = grupo.obtener(uid)
    except DatosException as e:
        return exception.HTTPNotFound()
    except Exception as e:
        log.error(e)
        return exception.HTTPInternalServerError()

    return {'mensaje': contenido}
    
