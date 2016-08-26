# coding: utf-8

from pyramid.view import view_config
from pyramid import httpexceptions as exception  

from ..juliette.grupos import Grupos

from cerberus import ValidationError

import logging
log = logging.getLogger('justine')

@view_config(route_name='grupos_listado', renderer='json', permission='listar')
def usuarios_listado(peticion):
    grupos = Grupos()
    contenido =  grupos.listar()[:150]
    return contenido
    
