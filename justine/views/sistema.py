# coding: utf-8

from pyramid.view import view_config
from pyramid import httpexceptions as exceptions

@view_config(route_name='logueo', renderer='json')
def login(peticion):
    datos = peticion.json_body
    usuario = datos['username']
    password = datos['password']
    
    # Acá va una función que hace magia, pero después, por favor
    user_id = usuario if usuario == password else False
    # Acá termina la función que hace magia

    if user_id:
        return {
            'result': 'OK',
            'token': peticion.create_jwt_token(user_id)
        }
    else:
        return {
            'result': 'ERROR',
        }
