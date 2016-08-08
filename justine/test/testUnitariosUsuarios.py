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

    def test_ficheros_listado(self):
        from ..views.usuarios import usuarios_listado
        peticion = testing.DummyRequest()
        respuesta = usuarios_listado(peticion)
        self.assertEqual(respuesta[0]['givenName'], "Rodrigo Arnoldo")
    
    def test_ficheros_listado_contador(self):
        from ..views.usuarios import usuarios_listado
        peticion = testing.DummyRequest()
        respuesta = usuarios_listado(peticion)
        self.assertTrue(len(respuesta) <= 250)
