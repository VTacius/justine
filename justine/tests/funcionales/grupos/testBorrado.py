# coding: utf-8

from unittest import TestCase
from ..modulos import cargar_datos, cargar_credenciales

import logging
log = logging.getLogger('justine')

class Borrado(TestCase):

    @classmethod
    def setUpClass(self):

        # Cargamos los datos
        entidad = cargar_datos('grupo')[0]
        self.uid = entidad['cn']
        self.datos = {'corpus': entidad}

        # Trabajamos en obtener un token
        self.token = cargar_credenciales()
        
        # Creamos nuestro objeto para pruebas
        from justine import main
        from webtest import TestApp

        app = main({})
        self.testapp = TestApp(app)
        
        self.testapp.post_json('/grupos', status=201, params=self.datos, headers=self.token)
    
    @classmethod
    def tearDownClass(self):
        res = self.testapp.head('/grupos/' + self.uid, status="*", headers=self.token)
        if res.status_int == 200:
            self.testapp.delete('/grupos/' + self.uid, status=200, headers=self.token)
    
    def test_borrado(self):
        res = self.testapp.delete('/grupos/' + self.uid, status=200, headers=self.token)
    
    def test_borrado_noexistente(self):
        uid = "fitzcarraldo"
        res = self.testapp.delete('/grupos/' + uid, status=404, headers=self.token)
    
    def test_borrado_noauth(self):
        res = self.testapp.delete('/grupos/' + self.uid, status=403)
    
