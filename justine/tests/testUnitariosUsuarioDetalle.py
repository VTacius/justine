# coding: utf-8

from unittest import TestCase
from pyramid import testing
from pyramid.registry import Registry
from pyramid.httpexceptions import HTTPForbidden, HTTPBadRequest

import logging
log = logging.getLogger('justine')

class Detalle(TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        self.config = testing.tearDown()

    def test_usuarios_detalle(self):
        from ..views.usuarios import usuarios_detalle
        
        peticion = testing.DummyRequest()
        peticion.matchdict = {'usuario': 'alortiz'}
        
        jwt_claims = {'rol': 'administrador'}
        peticion.jwt_claims = jwt_claims 

        respuesta = usuarios_detalle(peticion)
        self.assertEqual(respuesta['mensaje']['givenName'], 'Alexander')

    def test_usuarios_detalle_contador(self):
        from ..views.usuarios import usuarios_detalle

        peticion = testing.DummyRequest()
        peticion.matchdict = {'usuario': 'alortiz'}
        
        jwt_claims = {'rol': 'administrador'}
        peticion.jwt_claims = jwt_claims 
        
        respuesta = usuarios_detalle(peticion)
        self.assertTrue('mensaje' in respuesta)

    def test_usuarios_detalle_wrong_rol(self):
        from ..views.usuarios import usuarios_detalle

        peticion = testing.DummyRequest()
        peticion.matchdict = {'usuario': 'alortiz'}
        
        jwt_claims = {'rol': 'guerrillero'}
        peticion.jwt_claims = jwt_claims

        respuesta = usuarios_detalle(peticion)
        self.assertIsInstance(respuesta, HTTPForbidden)

    def test_usuarios_detalle_wrong_matchdict(self):
        from ..views.usuarios import usuarios_detalle

        peticion = testing.DummyRequest()
        peticion.matchdict = {'usuariaraje': 'alortiz'}

        respuesta = usuarios_detalle(peticion)
        self.assertIsInstance(respuesta, HTTPBadRequest)
