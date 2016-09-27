# coding: utf-8

from modulosFuncionales import credenciales

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
        
        self.token = credenciales('administrador')
        
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
        contenido_falso = 'Contenido falso'
        datos = {'corpus': {'uid': self.uid, clave_falsa: contenido_falso}}
        respuesta = self.testapp.patch_json('/usuarios/' + self.uid, status=400, params=datos, headers=self.token)
       
        self.assertRegexpMatches(str(respuesta.json_body), "{}\'\: \'unknown field".format(clave_falsa))

    def test_modificacion_usuarios_agregando_clave(self):
        datos = {'corpus': {'uid': self.uid, 'title': 'Sombrerero'}}
        self.testapp.patch_json('/usuarios/' + self.uid, status=200, params=datos, headers=self.token)
        
        respuesta = self.testapp.get('/usuarios/' + self.uid, status=200, headers=self.token)
        
        self.assertEqual(respuesta.json_body['mensaje']['title'], datos['corpus']['title'])
    
    def test_modificacion_usuarios_rol_usuario_otro_usuario(self):
        token = credenciales('usuario')
        datos = {'corpus': {'uid': self.uid, 'title': 'Sombrerero'}}
        
        respuesta = self.testapp.patch_json('/usuarios/' + self.uid, status=403, params=datos, headers=token)
        
        self.assertRegexpMatches(str(respuesta.json_body), "no puede modificar a {}".format(self.uid))

    def test_modificacion_usuarios_rol_tecnico_otro_usuario(self):
        token = credenciales('tecnicosuperior')
        datos = {'corpus': {'uid': self.uid, 'title': 'Sombrerero'}}

        respuesta = self.testapp.patch_json('/usuarios/' + self.uid, status=403, params=datos, headers=token)

        self.assertRegexpMatches(str(respuesta.json_body), "no puede modificar a {}".format(self.uid))
    
    def test_modificacion_usuarios_modificacion_usuario_mismatch(self):
        usuario = 'fitzcarraldo'
        datos = {'corpus': {'uid': self.uid, 'title': 'Sombrerero'}}
        
        respuesta = self.testapp.patch_json('/usuarios/' + usuario, status=400, params=datos, headers=self.token)
        
        self.assertRegexpMatches(str(respuesta.json_body), 'Usuarios de contenido y .+ no coinciden')
