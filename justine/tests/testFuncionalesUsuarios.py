# coding: utf-8

import logging
log = logging.getLogger('justine')

from unittest import TestCase

class Listado(TestCase):
    def setUp(self):
        from justine import main
        from webtest import TestApp

        app = main({})
        self.testapp = TestApp(app)

    def test_usuarios_listado(self):
        respuesta = self.testapp.get('/usuarios', status=200, xhr=True)
        self.assertEqual(respuesta.json_body[0]['givenName'], "Rodrigo Arnoldo")

class Detalle(TestCase):
    def setUp(self):
        self.maxDiff =  None
        from justine import main
        from webtest import TestApp

        app = main({})
        self.testapp = TestApp(app)

        # TODO: Podrías hacer esto menos público
        self.credenciales = {'username': 'vtacius', 'password': 'vtacius'}
        
        # No pos, nos ahorramos dos líneas en cada método, pos
        auth = self.testapp.post_json('/auth/login', status=200, params=self.credenciales)
        self.token = {'www-authorization': str(auth.json_body['token'])}
        
    def test_usuarios_detalle_unauth(self):
        respuesta = self.testapp.get('/usuarios/alortiz', status=403, xhr=True)
        self.assertRegexpMatches(respuesta.body, 'Access was denied to this resource')

    def test_usuarios_detalle(self):
        respuesta = self.testapp.get('/usuarios/alortiz', status=200, xhr=True, headers=self.token)
        self.assertEqual(respuesta.json_body['mensaje']['givenName'], 'Alexander')

    def test_usuarios_detalle_atributos(self):
        respuesta = self.testapp.get('/usuarios/alortiz', status=200, xhr=True, headers=self.token)
        atributos = respuesta.json_body['mensaje'].keys()
        claves = ["buzonStatus", "cuentaStatus", "dui", "fecha", "givenName", 
            "grupo", "grupos", "jvs", "loginShell", "mail", "nit", "o", "ou", 
            "pregunta", "respuesta", "sambaAcctFlags", "sn", "telephoneNumber", 
            "title", "uid", "userPassword", "usoBuzon", "volumenBuzon"]
        self.assertItemsEqual(sorted(atributos), sorted(claves))
    
    def test_usuarios_detalle_noexistente(self):
        respuesta = self.testapp.get('/usuarios/fitzcarraldo', status=404, xhr=True, headers=self.token)
        self.assertEqual(respuesta.status_code, 404)

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
    
    @classmethod
    def tearDownClass(self):
        self.testapp.delete('/usuarios/' + self.uid, status=200)

    def test_creacion_usuarios(self):

        respuesta = self.testapp.post_json('/usuarios', status=201, params=self.datos)
       
        self.assertEqual(respuesta.status_int, 201)
    
    def test_creacion_usuarios_existente(self):
        datos = self.datos
        datos['uid'] = 'alortiz'

        respuesta = self.testapp.post_json('/usuarios', status=409, params=self.datos)
        
        self.assertEqual(respuesta.status_int, 409)
    
    def test_creacion_usuarios_peticion_malformada(self):
        datos = "Mínimo esfuerzo para máximo daño"

        respuesta = self.testapp.post_json('/usuarios', status=400, params=datos)

        self.assertEqual(respuesta.status_int, 400)

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

        # Creamos un usuarios que luego vamos a borrar, al menos un mi mente así funciona estas cosas
        self.testapp.post_json('/usuarios', status=201, params=self.datos)
    
    def test_borrado_usuarios(self):
        respuesta = self.testapp.delete('/usuarios/' + self.uid, status=200)

        self.assertEqual(respuesta.status_int, 200)
   
    def test_borrado_usuarios_inexistente(self):
        self.uid = "fitzcarraldo"

        respuesta = self.testapp.delete('/usuarios/' + self.uid, status=404)

        self.assertEqual(respuesta.status_int, 404)

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
        
        # Creamos un usuario totalmente diferente a todo lo creado, estoy casi seguro que esta parte si debe funcionar de esta forma
        self.testapp.post_json('/usuarios', status=201, params=self.datos)
    
    @classmethod
    def tearDownClass(self):
        self.testapp.delete('/usuarios/' + self.uid, status=200)   
     
    def test_actualizacion_usuarios(self):
        datos = self.datos
        datos['corpus']['givenName'] = 'Claudia Carolina'
        datos['corpus']['sn'] = 'Peña Nieto'

        respuesta = self.testapp.put_json('/usuarios/' + self.uid, status=200, params=datos)

        self.assertEqual(respuesta.status_int, 200)

    def test_actualizacion_usuarios_noexistente(self):
        datos = self.datos
        uid = datos['corpus']['uid'] = 'fitzcarraldo'

        respuesta = self.testapp.put_json('/usuarios/' + uid, status=404, params=datos)
    
        self.assertEqual(respuesta.status_int, 404)
    
    def test_actualizacion_usuarios_uid_nocoincidente(self):
        datos = self.datos
        datos['corpus']['uid'] = 'fitzcarraldo' 

        respuesta = self.testapp.put_json('/usuarios/' + self.uid, status=400, params=datos)
        
        self.assertEqual(respuesta.status_int, 400)
    
    def test_actualizacion_usuarios_uid_peticion_malformada(self):
        datos = 'Mínimo esfuerzo para máximo daño'
        self.datos['corpus']['uid'] = 'cpena'
        self.uid = 'cpena'

        respuesta = self.testapp.put_json('/usuarios/' + self.uid, status=400, params=datos)

        self.assertEqual(respuesta.status_int, 400)

    def test_actualizacion_usuarios_claves_incompletas(self):
        sn = 'Castro Ortega'
        datos = {'corpus': {'uid': self.uid, 'sn': sn}}

        self.testapp.put_json('/usuarios/' + self.uid, status=400, params=datos)

class Modificacion(TestCase):
    
    @classmethod
    def setUpClass(self):
        self.uid = 'mrevelo'
        self.datos = {'corpus': {'uid': self.uid, 'sn':'Mendoza', 'givenName': 'Ana', 'o': {'nombre': 'Secretaría de Estado SS Ministerio de Salud', 'id': 1038}}}
        
        from justine import main
        from webtest import TestApp

        app = main({})
        self.testapp = TestApp(app)
        
        self.testapp.post_json('/usuarios', status=201, params=self.datos)

        # TODO: Podrías hacer esto menos público
        self.credenciales = {'username': 'vtacius', 'password': 'vtacius'}
        
        # No pos, nos ahorramos dos líneas en cada método, pos
        auth = self.testapp.post_json('/auth/login', status=200, params=self.credenciales)
        self.token = {'www-authorization': str(auth.json_body['token'])}

    @classmethod
    def tearDownClass(self):
        self.testapp.delete('/usuarios/' + self.uid, status=200) 

    def test_modificacion_usuarios(self):
        datos = {'corpus': {'uid': self.uid, 'sn': 'Mendoza Castro', 'givenName': 'Anita'}}
        respuesta = self.testapp.patch_json('/usuarios/' + self.uid, status=200, params=datos)

        self.assertEqual(respuesta.status_int, 200) 

    def test_modificacion_usuarios_noexistente(self):
        uid = 'fitzcarraldo'
        datos = {'corpus': {'uid': uid, 'sn': 'Mendoza Castro', 'givenName': 'Anita'}}
        
        respuesta = self.testapp.patch_json('/usuarios/' + uid, status=404, params=datos)
        
        self.assertEqual(respuesta.status_int, 404)

    def test_modificacion_usuarios_verificacion(self):
        datos = {'corpus': {'uid': self.uid, 'sn': 'Mendoza Castro', 'givenName': 'Anita'}}
        self.testapp.patch_json('/usuarios/' + self.uid, status=200, params=datos)

        respuesta = self.testapp.get('/usuarios/' + self.uid, status=200, headers=self.token)

        self.assertEqual(respuesta.json_body['mensaje']['sn'], datos['corpus']['sn'])

    def test_modificacion_usuarios_nopermitido_clave(self):
        clave_falsa = 'espejismo'
        datos = {'corpus': {'uid': self.uid, clave_falsa: 'Clave fantasmal'}}
        self.testapp.patch_json('/usuarios/' + self.uid, status=200, params=datos)
       
        respuesta = self.testapp.get('/usuarios/' + self.uid, status=200, headers=self.token)

        self.assertFalse(clave_falsa in respuesta.json_body['mensaje']) 
    

    def test_modificacion_usuarios_agregando_clave(self):
        datos = {'corpus': {'uid': self.uid, 'title': 'sobrerero'}}
        self.testapp.patch_json('/usuarios/' + self.uid, status=200, params=datos)
        
        respuesta = self.testapp.get('/usuarios/' + self.uid, status=200, headers=self.token)
        
        self.assertEqual(respuesta.json_body['mensaje']['title'], datos['corpus']['title'])
        
