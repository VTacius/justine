# coding: utf-8

from unittest import TestCase
from ..modulos import cargar_datos, cargar_credenciales

import logging
log = logging.getLogger('justine')

class Creacion(TestCase):
    """
    NOTA: Sobre la validación de datos, testar directamente nuestra pequeña clase 
    """

    @classmethod
    def setUp(self):

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

    @classmethod
    def tearDownClass(self):
        res = self.testapp.head('/grupos/' + self.uid, status="*", headers=self.token)
        if res.status_int == 200:
            self.testapp.delete('/grupos/' + self.uid, status=200, headers=self.token)
        self.datos = {}

    def test_creacion(self):
        res = self.testapp.post_json('/grupos', status=201, params=self.datos, headers=self.token)
        respuesta = res.location
        self.assertEqual(respuesta, 'http://localhost/grupos/%s' % self.uid)

    def test_creacion_no_json(self):
        datos = "Mínimo esfuerzo para máximo daño"
        self.testapp.post_json('/grupos', status=400, params=datos, headers=self.token)

    def test_creacion_corpus_faltante(self):
        datos = {'cuerpo': self.datos['corpus'].copy()}
        
        self.testapp.post_json('/grupos', status=400, params=datos, headers=self.token)

    def test_creacion_usuario_existente(self):
        self.testapp.post_json('/grupos', status=409, params=self.datos, headers=self.token)

    def test_usuarios_creacion_unauth(self):
        self.testapp.post_json('/grupos', status=403, params=self.datos)

