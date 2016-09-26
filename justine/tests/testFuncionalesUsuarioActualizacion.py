# coding: utf-8

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
        
        # TODO: Podrías hacer esto menos público
        self.credenciales = {'email': 'vtacius', 'password': 'vtacius'}
        
        # No pos, nos ahorramos dos líneas en cada método, pos
        auth = self.testapp.post_json('/auth/login', status=200, params=self.credenciales)
        self.token = {'www-authorization': str(auth.json_body['token'])}

        # Creamos un usuario totalmente diferente a todo lo creado, estoy casi seguro que esta parte si debe funcionar de esta forma
        self.testapp.post_json('/usuarios', status=201, params=self.datos, headers=self.token)
    
    @classmethod
    def tearDownClass(self):
        self.testapp.delete('/usuarios/' + self.uid, status=200, headers=self.token)   
     
    def test_actualizacion_usuarios(self):
        datos = self.datos
        datos['corpus']['givenName'] = 'Claudia Carolina'
        datos['corpus']['sn'] = 'Peña Nieto'

        respuesta = self.testapp.put_json('/usuarios/' + self.uid, status=200, params=datos, headers=self.token)

        self.assertEqual(respuesta.status_int, 200)

    def test_actualizacion_usuarios_noexistente(self):
        datos = self.datos
        uid = datos['corpus']['uid'] = 'fitzcarraldo'

        respuesta = self.testapp.put_json('/usuarios/' + uid, status=404, params=datos, headers=self.token)
    
        self.assertEqual(respuesta.status_int, 404)
    
    def test_actualizacion_usuarios_uid_nocoincidente(self):
        datos = self.datos
        datos['corpus']['uid'] = 'fitzcarraldo' 

        respuesta = self.testapp.put_json('/usuarios/' + self.uid, status=400, params=datos, headers=self.token)
        
        self.assertEqual(respuesta.status_int, 400)
    
    def test_actualizacion_usuarios_uid_peticion_malformada(self):
        datos = 'Mínimo esfuerzo para máximo daño'
        self.datos['corpus']['uid'] = 'cpena'
        self.uid = 'cpena'

        respuesta = self.testapp.put_json('/usuarios/' + self.uid, status=400, params=datos, headers=self.token)

        self.assertEqual(respuesta.status_int, 400)

    def test_actualizacion_usuarios_claves_incompletas(self):
        sn = 'Castro Ortega'
        datos = {'corpus': {'uid': self.uid, 'sn': sn}}

        self.testapp.put_json('/usuarios/' + self.uid, status=400, params=datos, headers=self.token)

