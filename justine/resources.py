from pyramid.security import Allow, Everyone, Authenticated

class Root(object):

    __acl__ = [
        (Allow, Authenticated, 'listar'),
        (Allow, Authenticated, 'detallar'),
        (Allow, 'administrador', 'creacion'),
        (Allow, 'administrador', 'actualizacion'),
        (Allow, 'administrador', 'borrado'),
        (Allow, Authenticated, 'modificacion')
    ]

    def __init__(self, request):
        pass
