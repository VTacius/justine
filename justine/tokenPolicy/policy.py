# coding: utf-8

import hmac
from json import dumps, loads
from base64 import b64encode,b64decode
from Crypto.Hash import SHA256
from Crypto.Cipher import AES

import warnings
from zope.interface import implementer
from pyramid.security import Everyone, Authenticated
from pyramid.interfaces import IAuthenticationPolicy

import logging
log = logging.getLogger('justine_token')

@implementer(IAuthenticationPolicy)
class TOKENAuthenticationPolicy(object):

    def __init__(self, **settings):
        self.http_header = settings.get('http_header', 'www-authorization')
        self.clave_privada = settings.get('clave_privada').encode()
        self.clave_generadora = settings.get('clave_generadora', 'This is an IV456')

    def remember(self, request, principal, **kw):
        warnings.warn(
            'JWT tokens need to be returned by an API. Using remember() '
            'has no effect.',
            stacklevel=3)
        return []

    def forget(self, request):
        warnings.warn(
            'JWT tokens are managed by API (users) manually. Using forget() '
            'has no effect.',
            stacklevel=3)
        return []

    def unauthenticated_userid(self, request):
        # TODO: ¿Cuál debería ser la verdadera implementación de esto?, ¿Para que sirve? (¿Disponible en request?)
        return request.get_token_claims.get('usuario')

    def authenticated_userid(self, request):
        # TODO: ¿Cuál debería ser la verdadera implementación de esto?
        return request.get_token_claims.get('direccion')

    def effective_principals(self, request):
        # Los principal se consiguen en el mismo token
        rol = request.get_token_claims.get('rol', False)
        if rol:
            principals = [Authenticated, rol]
        else: 
            principals = []
        return principals
   
    def crear_firma(self, mensaje):
        hmc = hmac.new(key=self.clave_privada, msg=mensaje, digestmod=SHA256)
        return b64encode(hmc.digest()).decode()

    def create_token(self, direccion, rol):
        """ 
        Creamos un token hmac con un contenido que por ahora incluye direccion (IP Address) y rol
        """
        contenido = dumps({'direccion': direccion, 'rol': rol}).encode()
        mensaje = b64encode(contenido).decode()
        
        firma = self.crear_firma(mensaje)
        
        token = '{0}.{1}'.format(mensaje, firma)
        return token
    
    def get_claims(self, request):
        # No vayas a usar Authorization, que son otros cinco pesos
        # TODO: No estoy verificando la ip del servidor, cuando así debería ser
        token = request.headers.get(self.http_header)
        if not token:
            return {}
        try: 
            mensaje, firma = token.split('.')
        except ValueError as e:
            # El token es inválido por no tener un punto de separación
            return {}
      
        firma_a_verificar = self.crear_firma(mensaje.encode())
        if firma_a_verificar == firma: 
            return loads(b64decode(mensaje))
        else:
            return {}
