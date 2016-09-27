# coding: utf-8
from pyramid.config import Configurator

# Configuramos seguridad
from pyramid.authorization import ACLAuthorizationPolicy
from .security import groupfinder

from pyramid.request import Request
from pyramid.response import Response

import logging
log = logging.getLogger('justine')

def request_factory(environ):
    environ['HTTP_ACCEPT'] = 'application/json' 
    request = Request(environ)
    request.response = Response()
    request.add_response_callback(finish_callback)
    return request

def finish_callback(peticion, respuesta):
    respuesta.headerlist.extend(
        (
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Headers', 'WWW-Authorization'),
            ('Access-Control-Allow-Headers', 'Content-Type'),
        )
    )
    return respuesta

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings, root_factory='.resources.Root')
    # Configuramos seguridad
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.include('pyramid_jwt')
    # Expira luego de 24 horas. Me pareció lo más indicado
    config.set_jwt_authentication_policy('c3cr3t0', http_header='www-authorization', callback=groupfinder, expiration=86400)
    # Rutas 
    # Rutas para logueo del sistema
    config.add_route('logueo', '/auth/login', request_method='POST')
    config.add_route('logueo_options', '/auth/login', request_method="OPTIONS")
    # Rutas para objeto ''helpers''
    config.add_route('helpers_establecimientos', '/helpers/establecimientos', request_method='GET')
    config.add_route('helpers_establecimientos_options', '/helpers/establecimientos', request_method='OPTIONS')
    config.add_route('helpers_oficinas', '/helpers/oficinas/{establecimiento}', request_method='GET')
    config.add_route('helpers_oficinas_options', '/helpers/oficinas/{establecimiento}', request_method='OPTIONS')
    # Rutas para objeto ''grupos''
    config.add_route('grupos_listado', '/grupos', request_method='GET')
    config.add_route('grupos_listado_options', '/grupos', request_method='OPTIONS')
    config.add_route('grupos_detalle', '/grupos/{grupo}', request_method='GET')
    # Rutas para objeto ''computadoras''
    config.add_route('computadoras_listado', '/computadoras', request_method='GET')
    config.add_route('computadoras_listado_options', '/computadoras', request_method='OPTIONS')
    # Rutas para objeto ''usuarios''
    config.add_route('usuarios_listado', '/usuarios', request_method='GET')
    config.add_route('usuarios_listado_options', '/usuarios', request_method='OPTIONS')
    config.add_route('usuarios_detalle', '/usuarios/{usuario}', request_method='GET')
    config.add_route('usuarios_creacion', '/usuarios', request_method='POST')
    config.add_route('usuarios_borrado', '/usuarios/{usuario}', request_method='DELETE')
    config.add_route('usuarios_actualizacion', '/usuarios/{usuario}', request_method='PUT')
    config.add_route('usuarios_actualizacion_options', '/usuarios/{usuario}', request_method='OPTIONS')
    config.add_route('usuarios_modificacion', '/usuarios/{usuario}', request_method='PATCH')
    config.scan()
    config.set_request_factory(request_factory)
    return config.make_wsgi_app()
