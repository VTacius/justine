# coding: utf-8

from pyramid.view import view_config
from pyramid import httpexceptions as exception

from ..juliette.computadoras import Computadoras

from cerberus import ValidationError
#from ..schemas.computadoras import EsquemaUsuario

import logging
log = logging.getLogger('justine')

@view_config(route_name='computadoras_listado', renderer='json', permission='listar')
def computadoras_listado(peticion):
    filtros = peticion.GET.dict_of_lists()
    computadoras = Computadoras()
    #if filtros:
    #    contenido = computadoras.busqueda(filtros) 
    #else:
    #    contenido = computadoras.listar()[:150]

    #return contenido

@view_config(route_name='computadoras_listado_options', renderer='json', permission='listar')
def computadoras_listado_options(peticion):
    pass
