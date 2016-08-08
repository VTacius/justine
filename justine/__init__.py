from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_route('home', '/')
    config.add_route('usuarios_listado', '/usuarios')
    config.add_route('usuarios_detalle', '/usuarios/{usuario}')
    config.scan()
    return config.make_wsgi_app()
