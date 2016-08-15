from pyramid.config import Configurator

# Configuramos seguridad
from pyramid.authorization import ACLAuthorizationPolicy
from .security import groupfinder


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings, root_factory='.resources.Root')
    # Configuramos seguridad
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.include('pyramid_jwt')
    config.set_jwt_authentication_policy('c3cr3t0', http_header='www-authorization', callback=groupfinder)
    # Rutas
    # Rutas para objeto ''usuarios''
    config.add_route('home', '/')
    config.add_route('logueo', '/login', request_method='POST')
    config.add_route('usuarios_listado', '/usuarios', request_method='GET')
    config.add_route('usuarios_detalle', '/usuarios/{usuario}', request_method='GET')
    config.add_route('usuarios_creacion', '/usuarios', request_method='POST')
    config.add_route('usuarios_borrado', '/usuarios/{usuario}', request_method='DELETE')
    config.add_route('usuarios_actualizacion', '/usuarios/{usuario}', request_method='PUT')
    config.add_route('usuarios_parchado', '/usuarios/{usuario}', request_method='PATCH')
    config.scan()
    return config.make_wsgi_app()
