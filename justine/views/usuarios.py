# coding: utf-8

from pyramid.view import view_config
from pyramid import httpexceptions as exception
from ..juliette.usuarios import Usuarios

from cerberus import Validator, ValidationError
from ..schemas.usuarios import EsquemaUsuario

import logging
log = logging.getLogger('justine')

@view_config(route_name='usuarios_listado', renderer='json', permission='listar')
def usuarios_listado(peticion):
    # Estamos probando seguridad
    usuarios = Usuarios()
    contenido = usuarios.listar()[:150]
    return contenido

@view_config(route_name='usuarios_detalle', renderer='json', permission='detallar')
def usuarios_detalle(peticion):
    # ¿Debe Colander entrar en acción en este punto?
    uid = peticion.matchdict['usuario']
    
    usuarios = Usuarios()
    try:
        contenido = {'data': usuarios.detalle(uid)}
    except Exception as e:
        return exception.HTTPNotFound()
    return contenido
    
@view_config(route_name="usuarios_creacion", renderer='json')
def usuarios_creacion(peticion):
   
    # Validando datos recibidos 
    v = EsquemaUsuario.obtener('creacion', 'uid', 'givenName', 'o', 'sn')
    try:
        contenido = v.validacion(peticion.json_body['corpus'])
    except ValidationError as e:
        return exception.HTTPBadRequest(e.args)
    except KeyError as e:
        return exception.HTTPBadRequest()

    usuarios = Usuarios()
    
    # Realizamos la operacion Creacion de Usuarios mediante la librería
    try:
        mensaje = usuarios.creacion(contenido)
    except IOError as e:
        # Si el usuario existe, devolvemos un 409 Conflict
        return exception.HTTPConflict()
    except Exception as e:
        # Ante cualquier otro error de la aplicación, 500 como debe ser pero más controlado
        # TODO: Ya que por ejemplo, en este lugar puedo hacer loggin
        return exception.HTTPInternalServerError()

    # La siguiente parece ser LA FORMA de responder en este caso
    # Sin embargo, mi response en este caso esta vació cuando se llama con un Request creado vacío
    # respuesta = peticion.response
    peticion.response.status_code = 201
    peticion.response.headerlist = [
         ('Location', str(mensaje)),
     ]
    return {'mensaje': mensaje}


@view_config(route_name='usuarios_borrado', renderer='json')
def usuarios_borrado(peticion):
    
    # Sin datos recibidos, no validación
    uid = peticion.matchdict['usuario'] 
     
    usuarios = Usuarios()
    
    # Realizamos la operacion Borrado de Usuarios mediante la librería
    try:
        mensaje = usuarios.borrado(uid)
    except ValueError as e:
        # Si el usuario no existe, devolvemos un 404 Not Found
        return exception.HTTPNotFound()
    except Exception as e:
        # Ante cualquier otro error de la aplicación, 500 como debe ser pero más controlado
        # TODO: Ya que por ejemplo, en este lugar puedo hacer loggin
        return exception.HTTPInternalServerError()

    return {'mensaje': mensaje}

@view_config(route_name='usuarios_actualizacion', renderer='json')
def usuarios_actualizacion(peticion):
    
    # Validando datos recibidos
    v = EsquemaUsuario.obtener('actualizacion', 'uid')
    try:
        uid = peticion.matchdict['usuario']
        contenido = peticion.json_body['corpus']
        # El corpus debe estar completo, y coincidir con el {usuario} que se peticiona a PUT
        if uid != contenido['uid']:
            raise KeyError
    except ValidationError as e:
        return exception.HTTPBadRequest(e.args)
    except KeyError as e:
        return exception.HTTPBadRequest()

    usuarios = Usuarios()

    # Realizamos la operacion de Actualización de Usuarios mediante la librería
    try:
        mensaje = usuarios.actualizacion(uid, contenido)
    except IOError as e:
        # Si el usuario no existe, devolvemos un 404 Not Found
        return exception.HTTPNotFound()
    except Exception as e:
        # Ante cualquier otro error de la aplicación, 500 como debe ser pero más controlado
        # TODO: Ya que por ejemplo, en este lugar puedo hacer loggin
        return exception.HTTPInternalServerError()
        
    return {'mensaje': mensaje}

@view_config(route_name='usuarios_modificacion', renderer='json')
def usuarios_modificacion(peticion):
    # Colander debe entrar en acción en este punto, las claves deben verificarse sin obligatoriedad
    
    try:
        uid = peticion.matchdict['usuario']
        contenido = peticion.json_body['corpus']
    except Exception as e:
        return exception.HTTPBadRequest()

    usuarios = Usuarios()
    
    try:
        mensaje = usuarios.modificacion(uid, contenido)
    except ValueError as e:
        # Si el usuario no existe, devolvemos un 404 Not Found
        return exception.HTTPNotFound()

    return {'mensaje': mensaje} 
