# coding: utf-8

from pyramid.view import view_config
from pyramid import httpexceptions as exception
from ..juliette.usuarios import Usuarios

@view_config(route_name='usuarios_listado', renderer='json')
def usuarios_listado(peticion):
    usuarios = Usuarios()
    contenido = usuarios.listar()[:150]
    return contenido

@view_config(route_name='usuarios_detalle', renderer='json')
def usuarios_detalle(peticion):
    usuarios = Usuarios()
    uid = peticion.matchdict['usuario']
    try:
        contenido = {'data': usuarios.detalle(uid)}
    except Exception as e:
        return exception.HTTPNotFound()

    return contenido
    
@view_config(route_name="usuarios_creacion", renderer='json')
def usuarios_creacion(peticion):
    usuarios = Usuarios()
    # Colander debe entrar en acción en este punto
    try:
        contenido = peticion.json_body['corpus']
    except Exception as e:
        return exception.HTTPBadRequest()

    # Es nuestra librería la que puede decirnos que el usuario ya existe o no
    try:
        contenido = usuarios.creacion(contenido)
    except IOError as e:
        return exception.exception_response(409)
    except Exception as e:
        return exception.exception_response(500)

    # La siguiente parece ser LA FORMA de responder en este caso
    # Sin embargo, mi response en este caso esta vació cuando se llama con un Request creado vacío
    # respuesta = peticion.response
    peticion.response.status_code = 201
    peticion.response.headerlist = [
         ('Location', str(contenido)),
     ]
    return {'mensaje': contenido}


@view_config(route_name='usuarios_borrado', renderer='json')
def usuarios_borrado(peticion):
    usuarios = Usuarios()
    
    uid = peticion.matchdict['usuario'] 
    
    try:
        contenido = usuarios.borrado(uid)
    except ValueError as e:
        return exception.exception_response(404)
    except Exception as e:
        return exception.exception_response(500)

    return {'mensaje': contenido}
