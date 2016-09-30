# coding: utf-8

from modulosFuncionales import credenciales

import logging
log = logging.getLogger('justine')

from unittest import TestCase

class Actualizacion(TestCase):

    @classmethod
    def setUpClass(self):
        self.uid = "cpena"
        self.datos = {"corpus": {"uid": self.uid, "sambaAcctFlags": True, "dui": "123456789-0", "title": "Gerente de Oficina", 
            "grupos": [1003, 1039, 1034], "usoBuzon": 150, "fecha": "1980-11-01", "mail": "cpena@salud.gob.sv", 
            "respuesta": "La misma de siempre", "loginShell": "false", "pregunta": "¿Cuál es mi pregunta?", "buzonStatus": True, 
            "grupo": 512, "nit": "4654-456546-142-3", "telephoneNumber": "7459", "cuentaStatus": True, "volumenBuzon": 500, 
            "o": {"nombre": "Secretaría de Estado SS Ministerio de Salud", "id": 1038}, "jvs": {"estado": False, "valor": None}, 
            "sn": "Peña", "ou": "Unidad Financiera Institucional", "givenName": "Carolina", "userPassword": "Abc_9999"}}
        
        from justine import main
        from webtest import TestApp
    
        app = main({})
        self.testapp = TestApp(app)
        
        self.token = credenciales('administrador') 

        # Creamos un usuario totalmente diferente a todo lo creado, estoy casi seguro que esta parte si debe funcionar de esta forma
        self.testapp.post_json('/usuarios', status=201, params=self.datos, headers=self.token)
    
    @classmethod
    def tearDownClass(self):
        self.testapp.delete('/usuarios/' + self.uid, status=200, headers=self.token)   
     
    def test_usuarios_actualizacion(self):
        datos = self.datos
        datos['corpus']['givenName'] = 'Claudia Carolina'
        datos['corpus']['sn'] = 'Peña Nieto'

        respuesta = self.testapp.put_json('/usuarios/' + self.uid, status=200, params=datos, headers=self.token)

        self.assertEqual(respuesta.status_int, 200)

    def test_usuarios_actualizacion_noexistente(self):
        datos = dict(self.datos)
        uid = datos['corpus']['uid'] = 'fitzcarraldo'

        respuesta = self.testapp.put_json('/usuarios/' + uid, status=404, params=datos, headers=self.token)
    
        self.assertEqual(respuesta.status_int, 404)
    
    def test_usuarios_actualizacion_uid_nocoincidente(self):
        datos = self.datos
        datos['corpus']['uid'] = 'fitzcarraldo' 

        respuesta = self.testapp.put_json('/usuarios/' + self.uid, status=400, params=datos, headers=self.token)
        
        self.assertEqual(respuesta.status_int, 400)
    
    def test_usuarios_actualizacion_uid_peticion_malformada(self):
        datos = 'Mínimo esfuerzo para máximo daño'

        respuesta = self.testapp.put_json('/usuarios/' + self.uid, status=400, params=datos, headers=self.token)

        self.assertEqual(respuesta.status_int, 400)

    def test_usuarios_actualizacion_claves_incompletas(self):
        sn = 'Castro Ortega'
        datos = {'corpus': {'uid': self.uid, 'sn': sn}}

        respuesta = self.testapp.put_json('/usuarios/' + self.uid, status=400, params=datos, headers=self.token)

    def test_usuarios_actualizacion_unauth(self):
        self.datos['corpus']['uid'] = self.uid
        
        respuesta = self.testapp.put_json('/usuarios/' + self.uid, status=403, params=self.datos)

        self.assertRegexpMatches(str(respuesta.json_body), 'Access was denied to this resource')
    
    def test_usuarios_actualizacion_rol_tecnico(self):
        self.datos['corpus']['uid'] = self.uid
        
        respuesta = self.testapp.put_json('/usuarios/' + self.uid, status=403, params=self.datos)

        self.assertRegexpMatches(str(respuesta.json_body), 'Access was denied to this resource')
    
    def test_usuarios_actualizacion_rol_usuario(self):
        self.datos['corpus']['uid'] = self.uid
        
        respuesta = self.testapp.put_json('/usuarios/' + self.uid, status=403, params=self.datos)

        self.assertRegexpMatches(str(respuesta.json_body), 'Access was denied to this resource')
