# coding: utf-8

from pyramid.view import view_config
from ..juliette.usuarios import Usuarios

@view_config(route_name='usuarios_listado', renderer='json')
def usuarios_listado(request):
    usuarios = Usuarios()
    return usuarios.listar()[:150]

