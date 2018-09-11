# coding: utf-8
from .policy import TOKENAuthenticationPolicy

def includeme(config):
    # Este es que permite que podamos hacr 
    config.add_directive(
        'set_token_authentication_policy',
        set_token_authentication_policy,
        action_wrap=True)


def create_token_authentication_policy(config, clave, http_header=None, callback=None):
    # TODO: Podemos poner un par de valores por defecto en esta acá en lugar de usar la policy
    # Al parecer, tener un config es necesario, en cuanto me permitiría acceder a configuraciones aparte
    #  más o menos de esta forma: private_key = private_key or settings.get('jwt.private_key')
    settings = config.get_settings()

    # TODO: clave_privada debería tener un valor por defecto

    return TOKENAuthenticationPolicy(clave_privada=clave, http_header=http_header)


def set_token_authentication_policy(config, clave, http_header=None):
    policy = create_token_authentication_policy(config, clave, http_header)

    def request_create_token(request, ip_address="127.0.0.1", rol="roleado"):
        return policy.create_token(ip_address, rol)

    def request_claims(request):
        return policy.get_claims(request)

    config.set_authentication_policy(policy)
    config.add_request_method(request_create_token, 'create_token')
    config.add_request_method(request_claims, 'get_token_claims', reify=True)
