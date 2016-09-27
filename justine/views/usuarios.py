# coding: utf-8

from pyramid.view import view_config
from pyramid import httpexceptions as exception

from ..juliette.usuarios import Usuarios
from ..juliette.Exceptions import RolInvalido, PermisosInsuficientes

from cerberus import ValidationError
from ..schemas.usuarios import EsquemaUsuario

import logging
log = logging.getLogger('justine')

@view_config(route_name='usuarios_listado', renderer='json', permission='listar')
def usuarios_listado(peticion):
    try:
        filtros = peticion.GET.dict_of_lists()
        rol = peticion.jwt_claims['rol']
        username = peticion.authenticated_userid
        usuarios = Usuarios.createAs(username, rol)
        if filtros:
            contenido = usuarios.busqueda(filtros) 
        else:
            contenido = usuarios.listar()[:250]
    except Exception as e:
        log.error(e)
        return exception.HTTPInternalServerError()

    return contenido

@view_config(route_name='usuarios_listado_options', renderer='json')
def usuarios_listado_options(peticion):
    pass

@view_config(route_name='usuarios_detalle', renderer='json', permission='detallar')
def usuarios_detalle(peticion):
    
    # Validando datos recibidos
    try:
        uid = peticion.matchdict['usuario'] 
    except KeyError as e:
        return exception.HTTPBadRequest()
    
    # Realizamos la operación Detalle de Usuarios mediante la librería
    try:
        rol = peticion.jwt_claims['rol']
        username = peticion.authenticated_userid
        usuarios = Usuarios.createAs(username, rol)
        contenido = usuarios.detalle(uid)
    except RolInvalido as e:
        return exception.HTTPForbidden(e.args)
    except IOError as e:
        return exception.HTTPNotFound()
    except Exception as e:
        log.error(e)
        return exception.HTTPInternalServerError()

    return {'mensaje': contenido}

@view_config(route_name='usuarios_borrado', renderer='json')
def usuarios_borrado(peticion):
    
    # Validando datos recibidos
    try:
        uid = peticion.matchdict['usuario'] 
    except KeyError as e:
        return exception.HTTPBadRequest()
     
    # Realizamos la operacion Borrado de Usuarios mediante la librería
    try:
        rol = peticion.jwt_claims['rol']
        username = peticion.authenticated_userid
        usuarios = Usuarios.createAs(username, rol)
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
        return exception.HTTPBadRequest()
    except ValidationError as e:
        return exception.HTTPBadRequest()
    except KeyError as e:
        return exception.HTTPBadRequest()
    except ValueError as e:
        return exception.HTTPBadRequest()

    # Realizamos la operacion Creacion de Usuarios mediante la librería
    try:
        rol = peticion.jwt_claims['rol']
        username = peticion.authenticated_userid
        usuarios = Usuarios.createAs(username, rol)
        mensaje = usuarios.creacion(contenido)
    except IOError as e:
        # Si el usuario existe, devolvemos un 409 Conflict
        return exception.HTTPConflict()
    except KeyError as e:
        # Ahora debería limitarse a que en jwt_claims no tenga 'rol'
        return exception.HTTPForbidden('atributos rol o username')
    except Exception as e:
        # Ante cualquier otro error de la aplicación, 500 como debe ser pero más controlado
        # TODO: Ya que por ejemplo, en este lugar puedo hacer loggin
        log.error('No puedo ver el error')
        return exception.HTTPInternalServerError()

    # La siguiente parece ser LA FORMA de responder en este caso
    # Sin embargo, mi response en este caso esta vació cuando se llama con un Request creado vacío
    peticion.response.status_code = 201
    peticion.response.headerlist.extend(
        (
            ('Location', str(mensaje)),
        )
    )

    return {'mensaje': mensaje}

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
        return exception.HTTPBadRequest()
    except ValidationError as e:
        log.error(e)
        return exception.HTTPBadRequest()
    except KeyError as e:
        log.error(e)
        return exception.HTTPBadRequest()
    except ValueError as e:
        log.error(e)
        return exception.HTTPBadRequest()

    # Realizamos la operacion de Actualización de Usuarios mediante la librería
    try:
        rol = peticion.jwt_claims['rol']
        username = peticion.authenticated_userid
        usuarios = Usuarios.createAs(username, rol)
        mensaje = usuarios.actualizacion(uid, contenido)
    except KeyError as e:
        log.error(e)
        # Si contenido enviado no tiene los datos del original
        return exception.HTTPBadRequest()
    except IOError as e:
        log.error(e)
        # Si el usuario no existe, devolvemos un 404 Not Found
        return exception.HTTPNotFound()
    except Exception as e:
        log.error(e)
        # Ante cualquier otro error de la aplicación, 500 como debe ser pero más controlado
        # TODO: Ya que por ejemplo, en este lugar puedo hacer loggin
        return exception.HTTPInternalServerError()
        
    return {'mensaje': mensaje}

@view_config(route_name='usuarios_actualizacion_options', renderer='json')
def usuarios_actualizacion_options(peticion):
    respuesta = peticion.response
    peticion.response.headerlist.extend(
        (
           ('Access-Control-Allow-Methods', 'PUT'), 
        )
    )
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
        return exception.HTTPBadRequest()
    except KeyError as e:
        return exception.HTTPBadRequest()
    except ValueError as e:
        return exception.HTTPBadRequest()

    # Realizamos la operación de Modificación de Usuarios mediante la librería    
    try:
        rol = peticion.jwt_claims['rol']
        username = peticion.authenticated_userid
        usuarios = Usuarios.createAs(username, rol)
        mensaje = usuarios.modificacion(uid, contenido)
    except IOError as e:
        # Si el usuario no existe, devolvemos un 404 Not Found
        return exception.HTTPNotFound()
    except PermisosInsuficientes as e:
        return exception.HTTPForbidden(e.args)
    except Exception as e:
        # Ante cualquier otro error de la aplicación, 500 como debe ser pero más controlado
        # TODO: Ya que por ejemplo, en este lugar puedo hacer loggin
        log.error(e)
        return exception.HTTPInternalServerError()

    return {'mensaje': mensaje} 
