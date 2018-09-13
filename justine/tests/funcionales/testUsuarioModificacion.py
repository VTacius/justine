# coding: utf-8

from modulosFuncionales import credenciales, cargar_datos, creador_test

import logging
log = logging.getLogger('justine')

from unittest import TestCase

class Modificacion(TestCase):
    
    @classmethod
    def setUpClass(self):
        contenido = cargar_datos('usuario')
        self.uid = contenido[3]['uid']
        self.datos = {"corpus": contenido[3]}

        from justine import main
        from webtest import TestApp

        app = main({})
        self.testapp = TestApp(app)
        
        self.token = credenciales('administrador')
        
        # Creamos un usuario sobre el cual trabajar
        self.testapp.post_json('/usuarios', status=201, params=self.datos, headers=self.token)

    @classmethod
    def tearDownClass(self):
        self.testapp.delete('/usuarios/' + self.uid, status=200, headers=self.token) 

    def test_usuarios_modificacion(self):
        datos = {'corpus': {'uid': self.uid, 'sn': 'Mendoza Castro', 'givenName': 'Anita'}}

        respuesta = self.testapp.patch_json('/usuarios/' + self.uid, status=200, params=datos, headers=self.token)

        self.assertEqual(respuesta.status_int, 200) 

    def test_usuarios_modificacion_noexistente(self):
        uid = 'fitzcarraldo'
        datos = {'corpus': {'uid': uid, 'sn': 'Mendoza Castro', 'givenName': 'Anita'}}
        
        respuesta = self.testapp.patch_json('/usuarios/' + uid, status=404, params=datos, headers=self.token)
        
        self.assertEqual(respuesta.status_int, 404)

    def test_usuarios_modificacion_verificacion(self):
        datos = {'corpus': {'uid': self.uid, 'sn': 'Mendoza Castro', 'givenName': 'Anita'}}
        self.testapp.patch_json('/usuarios/' + self.uid, status=200, params=datos, headers=self.token)

        respuesta = self.testapp.get('/usuarios/' + self.uid, status=200, headers=self.token)

        self.assertEqual(respuesta.json_body['mensaje'][0]['sn'], datos['corpus']['sn'])

    def test_usuarios_modificacion_nopermitido_clave(self):
        clave_falsa = 'espejismo'
        contenido_falso = 'Contenido falso'
        datos = {'corpus': {'uid': self.uid, clave_falsa: contenido_falso}}

        respuesta = self.testapp.patch_json('/usuarios/' + self.uid, status=400, params=datos, headers=self.token)
       

    def test_usuarios_modificacion_agregando_clave(self):
        datos = {'corpus': {'uid': self.uid, 'title': 'Sombrerero'}}
        self.testapp.patch_json('/usuarios/' + self.uid, status=200, params=datos, headers=self.token)
        
        respuesta = self.testapp.get('/usuarios/' + self.uid, status=200, headers=self.token)
       
        self.assertEqual(respuesta.json_body['mensaje'][0]['title'], datos['corpus']['title'])

    def test_usuarios_modificacion_unauth(self):
        datos = {'corpus': {'uid': self.uid, 'title': 'Sombrerero'}}

        log.error(self.uid)
        
        respuesta = self.testapp.patch_json('/usuarios/' + self.uid, status=403, params=datos)
        
        self.assertRegexpMatches(str(respuesta.json_body), 'Access was denied to this resource')
    
