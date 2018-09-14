# coding: utf-8

from unittest import TestCase
from ..modulos import cargar_datos, cargar_credenciales

import logging
log = logging.getLogger('justine')

class Borrado(TestCase):

    @classmethod
    def setUpClass(self):

        # Cargamos los datos
        entidad = cargar_datos('usuario')[0]
        self.uid = entidad['uid']
        self.datos = {'corpus': entidad}

        # Trabajamos en obtener un token
        self.token = cargar_credenciales()
        
        # Creamos nuestro objeto para pruebas
        from justine import main
        from webtest import TestApp

        app = main({})
        self.testapp = TestApp(app)
    
        self.testapp.post_json('/usuarios', status=201, params=self.datos, headers=self.token)
    
    @classmethod
    def tearDownClass(self):
        res = self.testapp.head('/usuarios/' + self.uid, status="*", headers=self.token)
        if res.status_int == 200:
            self.testapp.delete('/usuarios/' + self.uid, status=200, headers=self.token)
    
    def test_borrado(self):
        self.testapp.delete('/usuarios/' + self.uid, status=200, headers=self.token)
    
    def test_borrado_noexistente(self):
        uid = "fitzcarraldo"
        res = self.testapp.delete('/usuarios/' + uid, status=404, headers=self.token)
    
    def test_borrado_noauth(self):
        self.testapp.delete('/usuarios/' + self.uid, status=403)
