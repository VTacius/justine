# coding: utf-8

from pyramid.view import view_config
from pyramid import httpexceptions as exception

from ..juliette.helpers import Oficinas

from cerberus import ValidationError


import logging
log = logging.getLogger('justine')

@view_config(route_name='helpers_oficinas', renderer='json')
def oficinas_listado(peticion):
    establecimiento = peticion.matchdict['establecimiento']

    establecimientos = Oficinas()
    contenido = establecimientos.listar(establecimiento)
    return contenido
