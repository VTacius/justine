# coding: utf-8

from unittest import TestCase

class Listado(TestCase):
    def setUp(self):
        from justine import main
        from webtest import TestApp

        app = main({})
        self.testapp = TestApp(app)

    def test_ficheros_listado(self):
        respuesta = self.testapp.get('/usuarios', status=200, xhr=True)
        self.assertEqual(respuesta.json_body[0]['givenName'], "Rodrigo Arnoldo")
