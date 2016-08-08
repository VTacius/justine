from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_route('home', '/')
    config.add_route('usuarios_listado', '/usuarios', request_method='GET')
    config.add_route('usuarios_detalle', '/usuarios/{usuario}', request_method='GET')
    config.add_route('usuarios_creacion', '/usuarios', request_method='POST')
    config.scan()
    return config.make_wsgi_app()
