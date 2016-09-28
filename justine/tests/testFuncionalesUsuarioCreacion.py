# coding: utf-8

from modulosFuncionales import credenciales

import logging
log = logging.getLogger('justine')

from unittest import TestCase

class Creacion(TestCase):
    @classmethod
    def setUpClass(self):
        self.uid = "opineda"
        self.datos = {"corpus": {"uid": self.uid, "sambaAcctFlags": True, "dui": "123456789-0", "title": "Gerente de Oficina", 
            "grupos": [1003, 1039, 1034], "usoBuzon": 150, "fecha": "1980-11-01", "mail": "opineda@salud.gob.sv", 
            "respuesta": "La misma de siempre", "loginShell": "false", "pregunta": "¿Cuál es mi pregunta?", "buzonStatus": True, 
            "grupo": 512, "nit": "4654-456546-142-3", "telephoneNumber": "7459", "cuentaStatus": True, "volumenBuzon": 500, 
            "o": {"nombre": "Secretaría de Estado SS Ministerio de Salud", "id": 1038}, "jvs": {"estado": False, "valor": None}, 
            "sn": "Pineda", "ou": "Unidad Financiera Institucional", "givenName": "Olga", "userPassword": "Abc_9999"}}

        from justine import main
        from webtest import TestApp
        
        app = main({})
        self.testapp = TestApp(app)
    
        self.token = credenciales('administrador')
        
    @classmethod
    def tearDownClass(self):
        self.testapp.delete('/usuarios/' + self.uid, status=200, headers=self.token)

    def test_creacion_usuarios(self):

        respuesta = self.testapp.post_json('/usuarios', status=201, params=self.datos, headers=self.token)
       
        self.assertEqual(respuesta.status_int, 201)
    
    def test_creacion_usuarios_existente(self):
        datos = self.datos
        datos['uid'] = 'alortiz'

        respuesta = self.testapp.post_json('/usuarios', status=409, params=self.datos, headers=self.token)
        
        self.assertEqual(respuesta.status_int, 409)
    
    def test_creacion_usuarios_peticion_malformada(self):
        datos = "Mínimo esfuerzo para máximo daño"

        respuesta = self.testapp.post_json('/usuarios', status=400, params=datos, headers=self.token)

        self.assertEqual(respuesta.status_int, 400)

    def test_creacion_usuarios_unauth(self):
        respuesta = self.testapp.post_json('/usuarios', status=403, params=self.datos)

        self.assertEqual(respuesta.status_int, 403)

    def test_creacion_usuarios_rol_tecnico(self):
        token = credenciales('tecnicosuperior')
        respuesta = self.testapp.post_json('/usuarios', status=403, params=self.datos, headers=token)
        
        self.assertEqual(respuesta.status_int, 403)
    
    def test_creacion_usuarios_rol_usuario(self):
        token = credenciales('usuario')
        respuesta = self.testapp.post_json('/usuarios', status=403, params=self.datos, headers=token)
       
        self.assertRegexpMatches(str(respuesta.json_body), 'Access was denied to this resource')
