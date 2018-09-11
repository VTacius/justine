# coding: utf-8

import hmac
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
        self.clave_privada = settings.get('clave_privada')
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
        # TODO: ¿Cuál debería ser la verdadera implementación de esto?
        # Mi guía no tiene valor por defecto, aún así, no envia nada 
        # Recuerda que depende de self.get.claims, siendo configurado este como un método
        #  para request en __init__
        return request.get_token_claims.get('usuario')

    def authenticated_userid(self, request):
        # TODO: ¿Cuál debería ser la verdadera implementación de esto?
        return request.get_token_claims.get('usuario')

    def effective_principals(self, request):
        rol = request.get_token_claims.get('rol', False)
        if rol:
            principals = [Authenticated, rol]
        else: 
            principals = []
        return principals
    
    def encode_contenido(self, usuario, rol):
        cipher = AES.new(self.clave_generadora, AES.MODE_CFB, self.clave_generadora)
        try:
            contenido = '{0}.{1}'.format(usuario.encode('utf-8'), rol.encode('utf-8'))
        except UnicodeDecodeError as e:
            # Causado por el hecho de intentar cambiar el TOKEN
            return False
        return b64encode(cipher.encrypt(contenido))
    
    def decode_contenido(self, contenido):
        cipher = AES.new(self.clave_generadora, AES.MODE_CFB, self.clave_generadora)
        try:
            cifrado = cipher.decrypt(b64decode(contenido))
        except TypeError as e:
            # Incorrect padding: Cuando se ha modificado la longitud del token
            return ('', '')
        return cifrado.split('.')

    def create_token(self, usuario, rol):
        mensaje = self.encode_contenido(usuario, rol) 
        if not mensaje:
            return False
        # TODO: Debería ser msg=mensaje, lo que significa que no es cierto y hay que revisar exhaustivamente esto
        hmc = hmac.new(key=self.clave_privada, msg=usuario, digestmod=SHA256)
        hashito = b64encode(hmc.digest())
        
        token = '{0}.{1}'.format(mensaje, hashito)
        return token
    
    def get_claims(self, request):
        # No vayas a usar Authorization, que son otros cinco pesos
        token = request.headers.get(self.http_header)
        if not token:
            return {}
        try: 
            contenido, hmc = token.split('.')
            usuario, rol = self.decode_contenido(contenido)
        except ValueError as e:
            return {}
       
        token_a_verificar = self.create_token(usuario, rol)
        log.warning(token_a_verificar)
        log.warning(token)
        if  token_a_verificar == token: 
            return {'usuario': usuario, 'rol': rol}
        else:
            return {}
