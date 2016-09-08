# coding: utf-8

from pyramid.view import view_config
from pyramid import httpexceptions as exception

from ..juliette.helpers import Oficinas

from cerberus import ValidationError

import logging
log = logging.getLogger('justine')

@view_config(route_name='helpers_oficinas_options', renderer='json')
def oficinas_listado_options(peticion):
    pass

@view_config(route_name='helpers_oficinas', renderer='json')
def oficinas_listado(peticion):
    establecimiento = peticion.matchdict['establecimiento']

    establecimientos = Oficinas()

    try:
        contenido = establecimientos.listar(establecimiento)
    except IOError as e:
        return exception.HTTPNotFound()
    return contenido
