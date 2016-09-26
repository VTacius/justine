# coding: utf-8

import logging
log = logging.getLogger('justine')

from unittest import TestCase

class Modificacion(TestCase):
    
    @classmethod
    def setUpClass(self):
        self.uid = 'mrmarconi'
        self.datos = {'corpus': {'uid': self.uid, 'sn':'Mendoza', 'givenName': 'Ana', 'o': {'nombre': 'Secretaría de Estado SS Ministerio de Salud', 'id': 1038}}}
        
        from justine import main
        from webtest import TestApp

        app = main({})
        self.testapp = TestApp(app)
        
        # TODO: Podrías hacer esto menos público
        self.credenciales = {'email': 'vtacius', 'password': 'vtacius'}
        
        # No pos, nos ahorramos dos líneas en cada método, pos
        auth = self.testapp.post_json('/auth/login', status=200, params=self.credenciales)
        self.token = {'www-authorization': str(auth.json_body['token'])}
        
        # Creamos un usuario sobre el cual trabajar
        self.testapp.post_json('/usuarios', status=201, params=self.datos, headers=self.token)

    @classmethod
    def tearDownClass(self):
        self.testapp.delete('/usuarios/' + self.uid, status=200, headers=self.token) 

    def test_modificacion_usuarios(self):
        datos = {'corpus': {'uid': self.uid, 'sn': 'Mendoza Castro', 'givenName': 'Anita'}}
        respuesta = self.testapp.patch_json('/usuarios/' + self.uid, status=200, params=datos, headers=self.token)

        self.assertEqual(respuesta.status_int, 200) 

    def test_modificacion_usuarios_noexistente(self):
        uid = 'fitzcarraldo'
        datos = {'corpus': {'uid': uid, 'sn': 'Mendoza Castro', 'givenName': 'Anita'}}
        
        respuesta = self.testapp.patch_json('/usuarios/' + uid, status=404, params=datos, headers=self.token)
        
        self.assertEqual(respuesta.status_int, 404)

    def test_modificacion_usuarios_verificacion(self):
        datos = {'corpus': {'uid': self.uid, 'sn': 'Mendoza Castro', 'givenName': 'Anita'}}
        self.testapp.patch_json('/usuarios/' + self.uid, status=200, params=datos, headers=self.token)

        respuesta = self.testapp.get('/usuarios/' + self.uid, status=200, headers=self.token)

        self.assertEqual(respuesta.json_body['mensaje']['sn'], datos['corpus']['sn'])

    def test_modificacion_usuarios_nopermitido_clave(self):
        clave_falsa = 'espejismo'
        datos = {'corpus': {'uid': self.uid, clave_falsa: 'Clave fantasmal'}}
        self.testapp.patch_json('/usuarios/' + self.uid, status=200, params=datos, headers=self.token)
       
        respuesta = self.testapp.get('/usuarios/' + self.uid, status=200, headers=self.token)

        self.assertFalse(clave_falsa in respuesta.json_body['mensaje']) 

    def test_modificacion_usuarios_agregando_clave(self):
        datos = {'corpus': {'uid': self.uid, 'title': 'sobrerero'}}
        self.testapp.patch_json('/usuarios/' + self.uid, status=200, params=datos, headers=self.token)
        
        respuesta = self.testapp.get('/usuarios/' + self.uid, status=200, headers=self.token)
        
        self.assertEqual(respuesta.json_body['mensaje']['title'], datos['corpus']['title'])
        
