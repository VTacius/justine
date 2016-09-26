# coding: utf-8

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
        
        # TODO: Podrías hacer esto menos público
        self.credenciales = {'email': 'vtacius', 'password': 'vtacius'}
        
        # No pos, nos ahorramos dos líneas en cada método, pos
        auth = self.testapp.post_json('/auth/login', status=200, params=self.credenciales)
        self.token = {'www-authorization': str(auth.json_body['token'])}

        # Creamos un usuarios que luego vamos a borrar, al menos un mi mente así funciona estas cosas
        self.testapp.post_json('/usuarios', status=201, params=self.datos, headers=self.token)
    
    def test_borrado_usuarios(self):
        respuesta = self.testapp.delete('/usuarios/' + self.uid, status=200, headers=self.token)

        self.assertEqual(respuesta.status_int, 200)
   
    def test_borrado_usuarios_inexistente(self):
        self.uid = "fitzcarraldo"

        respuesta = self.testapp.delete('/usuarios/' + self.uid, status=404, headers=self.token)

        self.assertEqual(respuesta.status_int, 404)

