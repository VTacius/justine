# coding: utf-8

from pyramid.view import view_config
from pyramid import httpexceptions as exception  

from ..juliette.modelGroup import Grupo
from ..juliette.excepciones import DatosException, ConflictoException

from ..schemas.grupos import EsquemaGrupo

import logging
log = logging.getLogger(__name__)

@view_config(route_name="grupos_creacion", renderer='json', permission='creacion')
def grupos_creacion(peticion):
   
    # Validando datos recibidos 
    try:
        v = EsquemaGrupo('cn')
        contenido = v.validacion(peticion.json_body['corpus'])
    except KeyError as e:
        log.warning(e)
        return exception.HTTPBadRequest(e)
    except ValueError as e:
        log.warning(e)
        return exception.HTTPBadRequest(e)
    except TypeError as e:
        # Se refiere a que no se hayan enviado datos json correctamente formateados
        log.warning(e)
        return exception.HTTPBadRequest(e)
    except DatosException as e:
        log.warning(e)
        return exception.HTTPBadRequest(e)

    # Realizamos la operacion Creacion de Usuarios mediante la librería
    try:
        grupo = Grupo()
        cn_grupo = contenido['cn'].encode('ascii')
        contenido = grupo.crear(cn_grupo, contenido)
    except ConflictoException as e:
        # Si el grupo ya existe, devolvemos un 409 Conflict
        log.warning(e)
        return exception.HTTPConflict(e)
    except DatosException as e:
        log.warning('key error')
        log.warning(e)
        return exception.HTTPBadRequest(e)

    # La siguiente parece ser LA FORMA de responder en este caso
    # TODO: Sin embargo, mi response en este caso esta vació cuando se llama con un Request creado vacío
    peticion.response.status_code = 201
    peticion.response.headerlist.extend(
        (
            ('Location', "grupos/%s" % str(cn_grupo)),
        )
    )

    return {'mensaje': contenido}

@view_config(route_name='grupos_listado', renderer='json', permission='listar')
def grupos_listado(peticion):
    try:
        grupo = Grupo()
        contenido = grupo.obtener()
    except Exception as e:
        log.error(e)
        return exception.HTTPInternalServerError()
    print contenido
    return contenido

@view_config(route_name='grupos_listado_options', renderer='json')
def grupos_listado_options(peticion):
    pass

@view_config(route_name='grupos_detalle', renderer='json')
def grupos_detalle (peticion):
    
    try:
        uid = peticion.matchdict['grupo'] 
    except KeyError as e:
        return exception.HTTPBadRequest()
    
    # Realizamos la operación Detalle de Usuarios mediante la librería
    try:
        grupo = Grupo()
        contenido = grupo.obtener(uid)
    except DatosException as e:
        return exception.HTTPNotFound()
    except Exception as e:
        log.error(e)
        return exception.HTTPInternalServerError()

    return {'mensaje': contenido}
    
@view_config(route_name='grupos_borrado', renderer='json', permission='borrado')
def grupos_borrado(peticion):
    
    # Validando datos recibidos 
    try:
        v = EsquemaGrupo()
        cn_grupo = peticion.matchdict['grupo']
    except KeyError as e:
        log.warning(e)
        return exception.HTTPBadRequest(e)
    except TypeError as e:
        # Se refiere a que no se hayan enviado datos json correctamente formateados
        log.warning(e)
        return exception.HTTPBadRequest(e)
    except DatosException as e:
        log.warning(e)
        return exception.HTTPBadRequest(e)
    
    # Realizamos la operacion Borrado de Grupos mediante la librería
    try:
        grupo = Grupo()
        contenido = grupo.borrar(cn_grupo)
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
