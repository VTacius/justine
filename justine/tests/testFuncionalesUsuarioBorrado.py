# coding: utf-8

from modulosFuncionales import credenciales

import logging
log = logging.getLogger('justine')

from unittest import TestCase

class Borrado(TestCase):  

    @classmethod
    def setUpClass(self):
        self.uid = "lquevedo"
        self.datos = {"corpus": {"uid": self.uid, "sambaAcctFlags": True, "dui": "123456789-0", "title": "Gerente de Oficina", 
            "grupos": [1003, 1039, 1034], "usoBuzon": 150, "fecha": "1980-11-01", "mail": "lquevedo@salud.gob.sv", 
            "respuesta": "La misma de siempre", "loginShell": "false", "pregunta": "¿Cuál es mi pregunta?", "buzonStatus": True, 
            "grupo": 512, "nit": "4654-456546-142-3", "telephoneNumber": "7459", "cuentaStatus": True, "volumenBuzon": 500, 
            "o": {"nombre": "Secretaría de Estado SS Ministerio de Salud", "id": 1038}, "jvs": {"estado": False, "valor": None}, 
            "sn": "Quevedo", "ou": "Unidad Financiera Institucional", "givenName": "Laura", "userPassword": "Abc_9999"}}
        
        from justine import main
        from webtest import TestApp
        
        app = main({})
        self.testapp = TestApp(app)
        
        self.token = credenciales('administrador')

        # Creamos un usuarios que luego vamos a borrar, al menos un mi mente así funciona estas cosas
        self.testapp.post_json('/usuarios', status=201, params=self.datos, headers=self.token)
    
    def test_usuarios_borrado(self):
        respuesta = self.testapp.delete('/usuarios/' + self.uid, status=200, headers=self.token)

        self.assertEqual(respuesta.status_int, 200)
    
    def test_usuarios_borrado_inexistente(self):
        uid = "fitzcarraldo"

        respuesta = self.testapp.delete('/usuarios/' + uid, status=404, headers=self.token)

        self.assertEqual(respuesta.status_int, 404)

    def test_usuarios_borrado_unauth(self):
        respuesta = self.testapp.delete('/usuarios/' + self.uid, status=403)
        
        self.assertRegexpMatches(str(respuesta.json_body), 'Access was denied to this resource')

    def test_usuarios_borrado_rol_tecnico(self):
        token = credenciales('tecnicosuperior')

        respuesta = self.testapp.delete('/usuarios/' + self.uid, status=403, headers=token)

        self.assertRegexpMatches(str(respuesta.json_body), 'Access was denied to this resource')
    
    def test_usuarios_borrado_rol_usuario(self):
        token = credenciales('usuario')

        respuesta = self.testapp.delete('/usuarios/' + self.uid, status=403, headers=token)

        self.assertRegexpMatches(str(respuesta.json_body), 'Access was denied to this resource')
   

