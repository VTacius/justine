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
    
@view_config(route_name="usuarios_creacion", renderer='json')
def usuarios_creacion(request):
    usuarios = Usuarios()
    # Colander debe entrar en acción en este punto
    try:
        contenido = request.json_body['corpus']
    except Exception as e:
        return exception.HTTPBadRequest()

    # Es nuestra librería la que puede decirnos que el usuario ya existe o no
    try:
        contenido = usuarios.creacion(contenido)
    except Exception as e:
        return exception.exception_response(409)

    # La siguiente parece ser LA FORMA de responder en este caso
    respuesta = request.response
    respuesta.status_code = 201
    respuesta.headerlist = [
        ('Location', str(contenido)),
    ]
    return respuesta
    
    
