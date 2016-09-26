# coding: utf-8

from modulosFuncionales import credenciales

import logging
log = logging.getLogger('justine')

from unittest import TestCase

class Listado(TestCase):
    def setUp(self):
        from justine import main
        from webtest import TestApp

        app = main({})
        self.testapp = TestApp(app)
        
        # Obtenemos un token con credenciales de administrador 
        self.token = credenciales('administrador')

    def test_usuarios_listado_unauth(self):
        respuesta = self.testapp.get('/usuarios', status=403, xhr=True)
        self.assertRegexpMatches(respuesta.body, 'Access was denied to this resource')

    def test_usuarios_listado (self):
        respuesta = self.testapp.get('/usuarios', status=200, xhr=True, headers=self.token)
