# coding: utf-8

from pyramid.view import view_config
from pyramid import httpexceptions as exceptions

from ..juliette.conexion import parametros, credenciales, autenticacion
from ..juliette.excepciones import AutenticacionException
from ..juliette.modelBase import diccionador

import logging
log = logging.getLogger('justine')

@view_config(route_name='logueo_options', renderer='json')
def login_option(peticion):
    respuesta = peticion.response
    return {'mensaje': 'nada'}  

@view_config(route_name='logueo', renderer='json')
def login(peticion):
    # TODO: No, con este no autentico a la aplicación, este punto debe ser algo a usar
    #  por la otra aplicación para realmente autenticar a los usuarios
   
    try:
        datos = peticion.json_body
        usuario = datos['usuario'].encode('ascii')
        password = datos['password'].encode('ascii')
    except ValueError as e:
        return exceptions.HTTPBadRequest()
    except KeyError as e:
        return exceptions.HTTPBadRequest()  
    
    lp = parametros()
    creds = credenciales(usuario, password, lp)
    
    resultado = autenticacion(creds, lp)

    if (resultado):
        contenido = [diccionador([], u) for u in resultado]
    else:
        return exceptions.HTTPForbidden()

    INFORMACION = {
        'vtacius': ['Alexander Ortíz', 'administrador'],
        'alortiz': ['Alexander Ortega', 'tecnicosuperior'],
        'figaro': ['Estereotipo Estándar', 'tecnicoatencion'],
        'cpena': ['Estereotipo Secular', 'tecnicoatencion'],
        'kpenate': ['Estereotipo Secular', 'tecnicoatencion'],
        'usuario': ['Usuarios súper estándar', 'usuario']
    }


    datos_usuario = INFORMACION.get(usuario, [])

    rol = datos_usuario[1]

    return {
            'usuario': usuario,
            'gecos': datos_usuario[0],
            'permisos': datos_usuario[1],
            'token': peticion.create_token(usuario, rol)
            }
