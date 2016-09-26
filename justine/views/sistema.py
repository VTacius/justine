# coding: utf-8

from pyramid.view import view_config
from pyramid import httpexceptions as exceptions

# No tendría sentido que manejemos logggin desde tan abajo de la aplicación, que no sea en desarrollo
import logging
log = logging.getLogger('justine')

@view_config(route_name='logueo_options', renderer='json')
def login_option(peticion):
    respuesta = peticion.response
    return {'mensaje': 'nada'}  

@view_config(route_name='logueo', renderer='json')
def login(peticion):
   
    try:
        datos = peticion.json_body
    except ValueError as e:
        return exceptions.HTTPBadRequest()

    try:
        usuario = datos['email']
        password = datos['password']
    except KeyError as e:
        return exceptions.HTTPBadRequest()  
    
    # TODO: Voy a poner esto por acá para tomar datos, pero esto debería venir
    # de nuestra libreria juliette    
    # Luego sigue una que le envía al usuario los roles. Tenés que recordar que los 
    # roles los verificamos acá, le enviamos al cliente el rol para que el haga 
    # los use en su lógica
    INFORMACION = {
        'vtacius': ['Alexander Ortíz', 'administrador'],
        'alortiz': ['Alexander Ortega', 'tecnicosuperior'],
        'figaro': ['Estereotipo Estándar', 'tecnicoatencion'],
        'cpena': ['Estereotipo Secular', 'tecnicoatencion']
    }

    # Acá empieza la operación que permite autenticar a los usuarios
    try:
        # Acá va una función que hace magia, pero después, por favor
        user_id = usuario if usuario == password and usuario in INFORMACION else False
        # Acá termina la función que hace magia

        datos_usuario = INFORMACION.get(usuario, [])

        if user_id:
            return {
                'gecos': datos_usuario[0],
                'permisos': datos_usuario[1],
                'token': peticion.create_jwt_token(user_id, rol = datos_usuario[1])
            }
        else:
            return exceptions.HTTPUnauthorized()
    except Exception as e:
        return exceptions.HTTPInternalServerError()
