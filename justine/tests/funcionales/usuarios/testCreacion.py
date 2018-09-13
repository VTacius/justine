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

    @classmethod
    def tearDownClass(self):
        res = self.testapp.head('/usuarios/' + self.uid, status="*", headers=self.token)
        if res.status_int == 200:
            self.testapp.delete('/usuarios/' + self.uid, status=200, headers=self.token)

    def test_creacion(self):
        res = self.testapp.post_json('/usuarios', status=201, params=self.datos, headers=self.token)
        respuesta = res.location
        self.assertEqual(respuesta, 'http://localhost/usuarios/%s' % self.uid)

    def test_creacion_no_json(self):
        datos = "Mínimo esfuerzo para máximo daño"
        self.testapp.post_json('/usuarios', status=400, params=datos, headers=self.token)

    def test_creacion_corpus_faltante(self):
        datos = {'cuerpo': self.datos['corpus'].copy()}
        
        self.testapp.post_json('/usuarios', status=400, params=datos, headers=self.token)

    def test_creacion_usuario_existente(self):
        self.testapp.post_json('/usuarios', status=409, params=self.datos, headers=self.token)
   
    def test_creacion_usuario_datos_inconsistente(self):
        datos = self.datos.copy()
        datos['corpus']['grupo'] = "0"
        datos['corpus']['uid'] = "nuevoUsuario"
        
        self.testapp.post_json('/usuarios', status=400, params=datos, headers=self.token)

    def test_usuarios_creacion_unauth(self):
        self.testapp.post_json('/usuarios', status=403, params=self.datos)

