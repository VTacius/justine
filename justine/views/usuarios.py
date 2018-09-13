# coding: utf-8

from pyramid.view import view_config
from pyramid import httpexceptions as exception

from ..juliette.modelUser import Usuario
from ..juliette.excepciones import DatosException, ConflictoException

from ..schemas.usuarios import EsquemaUsuario

import logging
log = logging.getLogger(__name__)

@view_config(route_name="usuarios_creacion", renderer='json', permission='creacion')
def usuarios_creacion(peticion):
   
    # Validando datos recibidos 
    try:
        v = EsquemaUsuario('uid', 'givenName', 'o', 'sn', 'userPassword')
        contenido = v.validacion(peticion.json_body['corpus'])
    except KeyError as e:
        # No existe el corpus
        log.warning(e)
        return exception.HTTPBadRequest(e)
    except TypeError as e:
        # Se refiere a que no se hayan enviado datos json correctamente formateados
        log.warning(e)
        return exception.HTTPBadRequest(e)
    except DatosException as e:
        # En este punto, es nuestra librería de validación la que arroja un error
        log.warning(e)
        return exception.HTTPBadRequest(e)

    # Realizamos la operacion Creacion de Usuarios mediante la librería
    try:
        usuario = Usuario()
        username = contenido['uid'].encode('ascii')
        contenido = usuario.crear(username, contenido)
    except ConflictoException as e:
        # Si el usuario existe, devolvemos un 409 Conflict
        log.warning(e)
        return exception.HTTPConflict(e)
    except DatosException as e:
        # En este punto, estamos intentado configurar valores inválidos por inconsistencias 
        #  (Eje: Configurar como grupo principal a uno inexistente
        log.warning(e)
        return exception.HTTPBadRequest(e)

    # La siguiente parece ser LA FORMA de responder en este caso
    # TODO: Sin embargo, mi response en este caso esta vació cuando se llama con un Request creado vacío
    peticion.response.status_code = 201
    peticion.response.headerlist.extend(
        (
            ('Location', "usuarios/%s" % str(username)),
        )
    )

    return {'mensaje': contenido}

@view_config(route_name='usuarios_existente', renderer='json', permission='listar')
def usuarios_existente(peticion):
    try:
        uid = peticion.matchdict['usuario'] 
    except KeyError as e:
        # No existe el parametro usuario
        return exception.HTTPBadRequest()
    
    # Realizamos la operación Detalle de Usuarios mediante la librería
    try:
        usuario = Usuario()
        contenido = usuario.obtener(uid)
    except DatosException as e:
        return exception.HTTPNotFound()
    except Exception as e:
        log.error(e)
        return exception.HTTPInternalServerError()

    return {}

@view_config(route_name='usuarios_listado', renderer='json', permission='listar')
def usuarios_listado(peticion):
    try:
        usuario = Usuario()
        contenido = usuario.obtener()
    except Exception as e:
        log.error(e)
        return exception.HTTPInternalServerError()

    return contenido

@view_config(route_name='usuarios_listado_options', renderer='json')
def usuarios_listado_options(peticion):
    # TODO: ¿Es debido hacer algo acá?
    pass

@view_config(route_name='usuarios_detalle', renderer='json', permission='detallar')
def usuarios_detalle(peticion):
    
    try:
        uid = peticion.matchdict['usuario'] 
    except KeyError as e:
        # No existe el parametro usuario
        return exception.HTTPBadRequest()
    
    # Realizamos la operación Detalle de Usuarios mediante la librería
    try:
        usuario = Usuario()
        contenido = usuario.obtener(uid)
    except DatosException as e:
        return exception.HTTPNotFound()
    except Exception as e:
        log.error(e)
        return exception.HTTPInternalServerError()

    return {'mensaje': contenido}

@view_config(route_name='usuarios_actualizacion', renderer='json', permission='actualizacion')
def usuarios_actualizacion(peticion):
    
    # Luego vemos si es posible sobreescribir esto de ser necesario
    respuesta = peticion.response
    
    # Validando datos recibidos 
    try:
        v = EsquemaUsuario('uid')
        uid = peticion.matchdict['usuario']
        contenido = v.validacion(peticion.json_body['corpus'])
        # El corpus debe estar completo, y coincidir con el {usuario} que se peticiona a PUT
        if uid != contenido['uid']:
            return exception.HTTPBadRequest('Usuarios de contenido y petición no coinciden')
    except KeyError as e:
        # No existe el corpus
        log.warning(e)
        return exception.HTTPBadRequest(e)
    except TypeError as e:
        # Se refiere a que no se hayan enviado datos json correctamente formateados
        log.warning(e)
        return exception.HTTPBadRequest(e)
    except DatosException as e:
        # En este punto, es nuestra librería de validación la que arroja un error
        log.warning(e)
        return exception.HTTPBadRequest(e)
    
    # Realizamos la operacion Actualización (Con datos COMPLETOS) de Usuarios mediante la librería
    try:
        usuario = Usuario()
        username = contenido['uid'].encode('ascii')
        contenido = usuario.actualizar(username, contenido)
    except ConflictoException as e:
        # En este caso, conflicto viene a decir que no existe
        log.warning(e)
        return exception.HTTPNotFound(e)
    except DatosException as e:
        # Entre otras verificaciones sobre la integridad de los datos, se asegura que no quitemos datos
        #  (Esto se supone que es una convención para este punto de API)
        log.warning(e)
        return exception.HTTPBadRequest(e)
    except Exception as e:
        log.error(e)
        return exception.HTTPInternalServerError(e)
    
    return {'mensaje': contenido}

@view_config(route_name='usuarios_actualizacion_options', renderer='json')
def usuarios_actualizacion_options(peticion):
    respuesta = peticion.response
    peticion.response.headerlist.extend(
        (
           ('Access-Control-Allow-Methods', 'PUT'), 
        )
    )
    return {'mensaje': 'nada'}

@view_config(route_name='usuarios_modificacion', renderer='json', permission='modificacion')
def usuarios_modificacion(peticion):
    respuesta = peticion.response
    
    # Validando datos recibidos 
    try:
        v = EsquemaUsuario()
        username = peticion.matchdict['usuario']
        contenido = v.validacion(peticion.json_body['corpus'])
    except KeyError as e:
        # No existe el corpus o el parametro usuario
        log.warning(e)
        return exception.HTTPBadRequest(e)
    except TypeError as e:
        # Se refiere a que no se hayan enviado datos json correctamente formateados
        log.warning(e)
        return exception.HTTPBadRequest(e)
    except DatosException as e:
        # En este punto, es nuestra librería de validación la que arroja un error
        log.warning(e)
        return exception.HTTPBadRequest(e)
    
    # Realizamos la operacion Actualización (Con datos INCOMPLETOS) de Usuarios mediante la librería
    try:
        usuario = Usuario()
        contenido = usuario.actualizar(username, contenido, completo=False)
    except ConflictoException as e:
        # En este caso, conflicto viene a decir que no existe
        log.warning(e)
        return exception.HTTPNotFound(e)
    except DatosException as e:
        log.warning(e)
        return exception.HTTPBadRequest(e)
    except Exception as e:
        log.error(e)
        return exception.HTTPInternalServerError(e)
    
    return {'mensaje': contenido}

@view_config(route_name='usuarios_borrado', renderer='json', permission='borrado')
def usuarios_borrado(peticion):
    respuesta = peticion.response
    
    # Validando datos recibidos 
    try:
        v = EsquemaUsuario()
        username = peticion.matchdict['usuario']
    except KeyError as e:
        # No existe el corpus
        log.warning(e)
        return exception.HTTPBadRequest(e)
    except TypeError as e:
        # Se refiere a que no se hayan enviado datos json correctamente formateados
        log.warning(e)
        return exception.HTTPBadRequest(e)
    except DatosException as e:
        # En este punto, es nuestra librería de validación la que arroja un error
        log.warning(e)
        return exception.HTTPBadRequest(e)
    
    # Realizamos la operacion Borrado  Usuarios mediante la librería
    try:
        usuario = Usuario()
        contenido = usuario.borrar(username)
    except ConflictoException as e:
        # En este caso, conflicto viene a decir que no existe
        log.warning(e)
        return exception.HTTPNotFound(e)
    except DatosException as e:
        log.warning(e)
        return exception.HTTPBadRequest(e)
    except Exception as e:
        log.error(e)
        return exception.HTTPInternalServerError(e)

    return {'mensaje': contenido}
    
