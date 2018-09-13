# coding: utf-8

from unittest import TestCase
from ..modulos import cargar_datos, cargar_credenciales

import logging
log = logging.getLogger('justine')

class Detalle(TestCase):
    """
    NOTA: Sobre la validación de datos, testar directamente nuestra pequeña clase 
    """

    @classmethod
    def setUpClass(self):

        # Cargamos los datos
        entidad = cargar_datos('usuario')[1]
        self.uid = entidad['uid']
        self.datos = {'corpus': entidad}

        # Trabajamos en obtener un token
        self.token = cargar_credenciales()
        
        # Creamos nuestro objeto para pruebas
        from justine import main
        from webtest import TestApp

        app = main({})
        self.testapp = TestApp(app)

        res = self.testapp.post_json('/usuarios', status=201, params=self.datos, headers=self.token)

    @classmethod
    def tearDownClass(self):
        res = self.testapp.head('/usuarios/' + self.uid, status="*", headers=self.token)
        if res.status_int == 200:
            self.testapp.delete('/usuarios/' + self.uid, status=200, headers=self.token)

    def test_detalle_usuario(self):
        res = self.testapp.get('/usuarios/' + self.uid, status=200, headers=self.token) 
        respuesta = res.json_body['mensaje'][0]['givenName']
        datos = self.datos['corpus']['givenName']
        
        self.assertEqual(respuesta, datos)

    def test_detalle_noexistente(self):
        uid = 'fitzcarraldo'
        self.testapp.get('/usuarios/' + uid, status=404, headers=self.token)
        
    def test_detalle_unauth(self):
        self.testapp.post_json('/usuarios' + self.uid, status=404)
