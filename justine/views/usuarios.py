# coding: utf-8

from pyramid.view import view_config
from pyramid import httpexceptions as exception

from ..juliette.usuarios import Usuarios

from cerberus import ValidationError
from ..schemas.usuarios import EsquemaUsuario

import logging
log = logging.getLogger('justine')

@view_config(route_name='usuarios_listado', renderer='json', permission='listar')
def usuarios_listado(peticion):
    filtros = peticion.GET.dict_of_lists()
    usuarios = Usuarios()
    if filtros:
        contenido = usuarios.busqueda(filtros) 
    else:
        contenido = usuarios.listar()[:150]

    return contenido

#@view_config(route_name='usuarios_detalle', renderer='json', permission='detallar')
@view_config(route_name='usuarios_detalle', renderer='json')
def usuarios_detalle(peticion):
    
    # Validando datos recibidos
    try:
        uid = peticion.matchdict['usuario'] 
    except KeyError as e:
        return exception.HTTPBadRequest(headers=(('Access-Control-Allow-Origin', '*'),))
    
    usuarios = Usuarios()

    # Realizamos la operación Detalle de Usuarios mediante la librería
    try:
        contenido = usuarios.detalle(uid)
    except IOError as e:
        return exception.HTTPNotFound(headers=(('Access-Control-Allow-Origin', '*'),))
    except Exception as e:
        return exception.HTTPInternalServerError(headers=(('Access-Control-Allow-Origin', '*'),))

    return {'mensaje': contenido}

@view_config(route_name='usuarios_borrado', renderer='json')
def usuarios_borrado(peticion):
    
    # Validando datos recibidos
    try:
        uid = peticion.matchdict['usuario'] 
    except KeyError as e:
        return exception.HTTPBadRequest()
     
    usuarios = Usuarios()
    
    # Realizamos la operacion Borrado de Usuarios mediante la librería
    try:
        mensaje = usuarios.borrado(uid)
    except IOError as e:
        # Si el usuario no existe, devolvemos un 404 Not Found
        return exception.HTTPNotFound()
    except Exception as e:
        # Ante cualquier otro error de la aplicación, 500 como debe ser pero más controlado
        # TODO: Ya que por ejemplo, en este lugar puedo hacer loggin
        return exception.HTTPInternalServerError()

    return {'mensaje': mensaje}
    
@view_config(route_name="usuarios_creacion", renderer='json')
def usuarios_creacion(peticion):
   
    # Luego vemos si es posible sobreescribir esto de ser necesario
    respuesta = peticion.response
    
    # Validando datos recibidos 
    v = EsquemaUsuario.obtener('creacion', 'uid', 'givenName', 'o', 'sn')
    try:
        contenido = v.validacion(peticion.json_body['corpus'])
    except TypeError as e:
        return exception.HTTPBadRequest(headers=(('Access-Control-Allow-Origin', '*'),))
    except ValidationError as e:
        return exception.HTTPBadRequest(headers=(('Access-Control-Allow-Origin', '*'),))
    except KeyError as e:
        return exception.HTTPBadRequest(headers=(('Access-Control-Allow-Origin', '*'),))
    except ValueError as e:
        return exception.HTTPBadRequest(headers=(('Access-Control-Allow-Origin', '*'),))

    usuarios = Usuarios()
    
    # Realizamos la operacion Creacion de Usuarios mediante la librería
    try:
        mensaje = usuarios.creacion(contenido)
    except IOError as e:
        # Si el usuario existe, devolvemos un 409 Conflict
        return exception.HTTPConflict(headers=(('Access-Control-Allow-Origin', '*'),))
    except Exception as e:
        # Ante cualquier otro error de la aplicación, 500 como debe ser pero más controlado
        # TODO: Ya que por ejemplo, en este lugar puedo hacer loggin
        return exception.HTTPInternalServerError(headers=(('Access-Control-Allow-Origin', '*'),))

    # La siguiente parece ser LA FORMA de responder en este caso
    # Sin embargo, mi response en este caso esta vació cuando se llama con un Request creado vacío
    peticion.response.status_code = 201
    peticion.response.headerlist.extend(
        (
            ('Location', str(mensaje)),
        )
    )

    return {'mensaje': mensaje}

@view_config(route_name='usuarios_creacion_options', renderer='json')
def usuarios_creacion_options(peticion):
    respuesta = peticion.response
    log.error('Cabeceras para respuesta en option')
    log.error(respuesta.headerlist)
    return {'mensaje': 'nada'}

@view_config(route_name='usuarios_actualizacion', renderer='json')
def usuarios_actualizacion(peticion):
    
    # Validando datos recibidos
    v = EsquemaUsuario.obtener('actualizacion', 'uid')
    try:
        uid = peticion.matchdict['usuario']
        contenido = v.validacion(peticion.json_body['corpus'])
        # El corpus debe estar completo, y coincidir con el {usuario} que se peticiona a PUT
        if uid != contenido['uid']:
            raise KeyError('Usuarios de contenido y petición no coinciden')
    except TypeError as e:
        log.error(e)
        return exception.HTTPBadRequest(headers=(('Access-Control-Allow-Origin', '*'),))
    except ValidationError as e:
        log.error(e)
        return exception.HTTPBadRequest(headers=(('Access-Control-Allow-Origin', '*'),))
    except KeyError as e:
        log.error(e)
        return exception.HTTPBadRequest(headers=(('Access-Control-Allow-Origin', '*'),))
    except ValueError as e:
        log.error(e)
        return exception.HTTPBadRequest(headers=(('Access-Control-Allow-Origin', '*'),))

    usuarios = Usuarios()

    # Realizamos la operacion de Actualización de Usuarios mediante la librería
    try:
        mensaje = usuarios.actualizacion(uid, contenido)
    except KeyError as e:
        log.error(e)
        # Si contenido enviado no tiene los datos del original
        return exception.HTTPBadRequest(headers=(('Access-Control-Allow-Origin', '*'),))
    except IOError as e:
        log.error(e)
        # Si el usuario no existe, devolvemos un 404 Not Found
        return exception.HTTPNotFound(headers=(('Access-Control-Allow-Origin', '*'),))
    except Exception as e:
        log.error(e)
        # Ante cualquier otro error de la aplicación, 500 como debe ser pero más controlado
        # TODO: Ya que por ejemplo, en este lugar puedo hacer loggin
        return exception.HTTPInternalServerError(headers=(('Access-Control-Allow-Origin', '*'),))
        
    return {'mensaje': mensaje}

@view_config(route_name='usuarios_actualizacion_options', renderer='json')
def usuarios_actualizacion_options(peticion):
    respuesta = peticion.response
    log.error('Cabeceras para respuesta en option')
    peticion.response.headerlist.extend(
        (
           ('Access-Control-Allow-Methods', 'PUT'), 
        )
    )
    log.error(respuesta.headerlist)
    return {'mensaje': 'nada'}

@view_config(route_name='usuarios_modificacion', renderer='json')
def usuarios_modificacion(peticion):
   
    # Validando datos recibidos 
    v = EsquemaUsuario.obtener('modificacion', 'uid')
    try:
        uid = peticion.matchdict['usuario']
        contenido = peticion.json_body['corpus']
        # El corpus debe estar completo, y coincidir con el {usuario} que se peticiona a PUT
        if uid != contenido['uid']:
            raise KeyError('Usuarios de contenido y petición no coinciden')
    except ValidationError as e:
        return exception.HTTPBadRequest(e.args)
    except KeyError as e:
        return exception.HTTPBadRequest()
    except ValueError as e:
        return exception.HTTPBadRequest()

    usuarios = Usuarios()

    # Realizamos la operación de Modificación de Usuarios mediante la librería    
    try:
        mensaje = usuarios.modificacion(uid, contenido)
    except IOError as e:
        # Si el usuario no existe, devolvemos un 404 Not Found
        return exception.HTTPNotFound()
    except Exception as e:
        # Ante cualquier otro error de la aplicación, 500 como debe ser pero más controlado
        # TODO: Ya que por ejemplo, en este lugar puedo hacer loggin
        return exception.HTTPInternalServerError()

    return {'mensaje': mensaje} 
