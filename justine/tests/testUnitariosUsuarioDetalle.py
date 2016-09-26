# coding: utf-8

from unittest import TestCase
from pyramid import testing
from pyramid.registry import Registry
from json import dumps

import logging
log = logging.getLogger('justine')

class Detalle(TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        self.config = testing.tearDown()

    def test_usuarios_detalle(self):
        from ..views.usuarios import usuarios_detalle
        from pyramid.request import Request
        
        peticion = Request.blank('', {})
        peticion.matchdict = {'usuario': 'alortiz'}
        
        register = Registry('testing')
        peticion.registry = register
        
        jwt_claims = {'rol': 'administrador'}
        peticion.jwt_claims = jwt_claims 

        respuesta = usuarios_detalle(peticion)
        self.assertEqual(respuesta['mensaje']['givenName'], 'Alexander')

    def test_usuarios_detalle_contador(self):
        from ..views.usuarios import usuarios_detalle
        peticion = testing.DummyRequest
        
        jwt_claims = {'rol': 'administrador'}
        peticion.jwt_claims = jwt_claims 
        
        peticion.matchdict = {'usuario': 'alortiz'}
        respuesta = usuarios_detalle(peticion)
        self.assertTrue('mensaje' in respuesta)

