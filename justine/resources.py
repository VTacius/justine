from pyramid.security import Allow, Everyone, Authenticated

class Root(object):

    __acl__ = [
        (Allow, Everyone, 'listar'),
        (Allow, Authenticated, 'detallar'),
        (Allow, 'groups:admins', 'creacion'),
        (Allow, 'groups:editors', 'actualizacion'),
        (Allow, 'groups:admins', 'borrado'),
        (Allow, Authenticated, 'modificacion')
    ]

    def __init__(self, request):
        pass
