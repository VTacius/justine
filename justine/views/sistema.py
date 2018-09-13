# coding: utf-8

from pyramid.view import view_config
from pyramid import httpexceptions as exceptions
from pyramid.authentication import extract_http_basic_credentials

from ..juliette.conexion import parametros, credenciales, autenticacion
from ..juliette.excepciones import AutenticacionException
from ..juliette.modelBase import diccionador

import logging
log = logging.getLogger('justine')

# TODO: Se merece una mejor implementación que esto
USUARIOS_ADMIN = ['alortiz']

@view_config(route_name='logueo_options', renderer='json')
def login_option(peticion):
    respuesta = peticion.response
    return {'mensaje': 'nada'}  

@view_config(route_name='logueo', renderer='json', permission='login')
def login(peticion):
    """
    Considerar que este login sirve para que otra aplicación autentique a sus usuarios
    """
   
    try:
        datos = peticion.json_body
        usuario = datos['usuario'].encode('ascii')
        password = datos['password'].encode('ascii')
        log.warning(usuario)
        log.warning(password)
    except ValueError as e:
        return exceptions.HTTPBadRequest()
    except KeyError as e:
        return exceptions.HTTPBadRequest()  
   
    resultado = autenticar_en_samba(usuario, password)
    
    if (resultado):
        contenido = [diccionador([], u) for u in resultado]
        user_data = contenido[0]
    else:
        return exceptions.HTTPForbidden()

    g = user_data.get('memberOf', [])
    displayName = user_data.get('displayName', usuario)
    grupos = g if type(g) == list else [g]
    resultado =  { 'displayName': displayName, 'grupos':  grupos }
    
    return resultado 

def autenticar_en_samba(usuario, password):
    lp = parametros()
    creds = credenciales(usuario, password, lp)
    
    return autenticacion(creds, lp)


@view_config(route_name='logueo_crear_token', renderer='json')
def crear_token(peticion):
    credenciales = extract_http_basic_credentials(peticion)
    if credenciales:
        usuario, password = credenciales
        resultado = autenticar_en_samba(usuario, password)
        if resultado and usuario in USUARIOS_ADMIN:
            try:
                direccion = peticion.json_body['direccion']
                rol = peticion.json_body['rol']
            except:
                return exceptions.HTTPBadRequest()
            return {'token': peticion.create_token(direccion, rol)}
            
    return exceptions.HTTPForbidden()
