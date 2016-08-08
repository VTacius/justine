# coding: utf-8

from pyramid.view import view_config
from pyramid import httpexceptions as exception
from ..juliette.usuarios import Usuarios

@view_config(route_name='usuarios_listado', renderer='json')
def usuarios_listado(request):
    usuarios = Usuarios()
    contenido = usuarios.listar()[:150]
    return contenido

@view_config(route_name='usuarios_detalle', renderer='json')
def usuarios_detalle(request):
    usuarios = Usuarios()
    uid = request.matchdict['usuario']
    try:
        contenido = {'data': usuarios.detalle(uid)}
    except Exception as e:
        return exception.HTTPNotFound()

    return contenido
    

