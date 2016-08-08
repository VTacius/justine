# coding: utf-8

from unittest import TestCase
from pyramid import testing
from json import dumps

class Listado(TestCase):
    def setUp(self):
        self.maxDiff =  None
        self.config = testing.setUp()

    def tearDown(self):
        self.config = testing.tearDown()

    def test_usuarios_listado(self):
        from ..views.usuarios import usuarios_listado
        peticion = testing.DummyRequest()
        respuesta = usuarios_listado(peticion)
        self.assertEqual(respuesta[0]['givenName'], "Rodrigo Arnoldo")
    
    def test_usuarios_listado_contador(self):
        from ..views.usuarios import usuarios_listado
        peticion = testing.DummyRequest()
        respuesta = usuarios_listado(peticion)
        self.assertTrue(len(respuesta) <= 250)

class Detalle(TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        self.config = testing.tearDown()

    def test_usuarios_detalle(self):
        from ..views.usuarios import usuarios_detalle
        peticion = testing.DummyRequest
        peticion.matchdict = {'usuario': 'alortiz'}
        respuesta = usuarios_detalle(peticion)
        self.assertEqual(respuesta['data']['givenName'], 'Alexander')

    def test_usuarios_detalle_contador(self):
        from ..views.usuarios import usuarios_detalle
        peticion = testing.DummyRequest
        peticion.matchdict = {'usuario': 'alortiz'}
        respuesta = usuarios_detalle(peticion)
        self.assertTrue('data' in respuesta)
