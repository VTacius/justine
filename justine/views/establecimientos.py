# coding: utf-8

from pyramid.view import view_config
from pyramid import httpexceptions as exception

from ..juliette.helpers import Establecimientos

from cerberus import ValidationError


import logging
log = logging.getLogger('justine')

@view_config(route_name='helpers_establecimientos', renderer='json')
def establecimientos_listado(peticion):
    establecimientos = Establecimientos()
    contenido = establecimientos.listar()
    return contenido
    
