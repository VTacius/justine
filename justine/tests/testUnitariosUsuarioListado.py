# coding: utf-8

from unittest import TestCase
from pyramid import testing
from pyramid.registry import Registry
from json import dumps

class Listado(TestCase):
    def setUp(self):
        self.maxDiff =  None
        self.config = testing.setUp()

    def tearDown(self):
        self.config = testing.tearDown()

    def test_usuarios_listado(self):
        pass
        #from ..views.usuarios import usuarios_listado
        #from pyramid.request import Request

        #peticion = Request.blank('', {})
        #
        #jwt_claims = {'rol': 'administrador'}
        #peticion.jwt_claims = jwt_claims 

        #respuesta = usuarios_listado(peticion)
        #
        #self.assertEqual(respuesta[0]['givenName'], "Baloncesto")
    
    def test_usuarios_listado_contador(self):
        pass
        #from ..views.usuarios import usuarios_listado
        #from pyramid.request import Request

        #peticion = Request.blank('', {})

        #jwt_claims = {'rol': 'administrador'}
        #peticion.jwt_claims = jwt_claims 

        #respuesta = usuarios_listado(peticion)
        #self.assertTrue(len(respuesta) <= 250)
