# coding: utf-8

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

    def test_usuarios_detalle(self):
        respuesta = self.testapp.get('/usuarios/alortiz', status=200, xhr=True)
        self.assertEqual(respuesta.json_body['data']['givenName'], 'Alexander')

    def test_usuarios_detalle_atributos(self):
        respuesta = self.testapp.get('/usuarios/alortiz', status=200, xhr=True)
        atributos = respuesta.json_body['data'].keys()
        claves = ["buzonStatus", "cuentaStatus", "dui", "fecha", "givenName", 
            "grupo", "grupos", "jvs", "loginShell", "mail", "nit", "o", "ou", 
            "pregunta", "respuesta", "sambaAcctFlags", "sn", "telephoneNumber", 
            "title", "uid", "userPassword", "usoBuzon", "volumenBuzon"]
        self.assertItemsEqual(sorted(atributos), sorted(claves))
    
    def test_usuarios_detalle_noexistente(self):
        respuesta = self.testapp.get('/usuarios/fitzcarraldo', status=404, xhr=True)
        self.assertEqual(respuesta.status_code, 404)

class Creacion(TestCase):
    @classmethod
    def setUpClass(self):
        self.uid = "opineda"
        self.datos = {"corpus": {"uid": self.uid, "sambaAcctFlags": True, "dui": "123456789-0", "title": "Gerente de Oficina", 
            "grupos": ["1003", "1039", "1034"], "usoBuzon": "150MB", "fecha": "01/11/1980", "mail": "opineda@salud.gob.sv", 
            "respuesta": "La misma de siempre", "loginShell": "false", "pregunta": "¿Cuál es mi pregunta?", "buzonStatus": True, 
            "grupo": "512", "nit": "4654-456546-142-3", "telephoneNumber": "7459", "cuentaStatus": True, "volumenBuzon": "500MB", 
            "o": {"nombre": "Secretaría de Estado SS Ministerio de Salud", "id": 1038}, "jvs": {"estado": True, "valor": None}, 
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
            "grupos": ["1003", "1039", "1034"], "usoBuzon": "150MB", "fecha": "01/11/1980", "mail": "lquevedo@salud.gob.sv", 
            "respuesta": "La misma de siempre", "loginShell": "false", "pregunta": "¿Cuál es mi pregunta?", "buzonStatus": True, 
            "grupo": "512", "nit": "4654-456546-142-3", "telephoneNumber": "7459", "cuentaStatus": True, "volumenBuzon": "500MB", 
            "o": {"nombre": "Secretaría de Estado SS Ministerio de Salud", "id": 1038}, "jvs": {"estado": True, "valor": None}, 
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
            "grupos": ["1003", "1039", "1034"], "usoBuzon": "150MB", "fecha": "01/11/1980", "mail": "cpena@salud.gob.sv", 
            "respuesta": "La misma de siempre", "loginShell": "false", "pregunta": "¿Cuál es mi pregunta?", "buzonStatus": True, 
            "grupo": "512", "nit": "4654-456546-142-3", "telephoneNumber": "7459", "cuentaStatus": True, "volumenBuzon": "500MB", 
            "o": {"nombre": "Secretaría de Estado SS Ministerio de Salud", "id": 1038}, "jvs": {"estado": True, "valor": None}, 
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
        datos['corpus']['giveName'] = 'Claudia Carolina'
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

    def test_actualizacion_usuarios_claves_completas(self):
        sn = 'Castro Ortega'
        datos = {'corpus': {'uid': self.uid, 'sn': sn}}

        self.testapp.put_json('/usuarios/' + self.uid, status=200, params=datos)

        respuesta = self.testapp.get('/usuarios/' + self.uid, status=200)

        claves = sorted(respuesta.json_body['data'].keys())
        claves_primarias = sorted(self.datos['corpus'].keys())

        self.assertEqual(claves, claves_primarias)

class Parchado(TestCase):
    
    @classmethod
    def setUpClass(self):
        self.uid = 'mrevelo'
        self.datos = {'corpus': {'uid': self.uid, 'sn':'Mendoza', 'givenName': 'Ana'}}
        
        from justine import main
        from webtest import TestApp

        app = main({})
        self.testapp = TestApp(app)
        
        self.testapp.post_json('/usuarios', status=201, params=self.datos)

    @classmethod
    def tearDownClass(self):
        self.testapp.delete('/usuarios/' + self.uid, status=200) 

    def test_parchado_usuarios(self):
        datos = {'corpus': {'sn': 'Mendoza Castro', 'givenName': 'Anita'}}
        respuesta = self.testapp.patch_json('/usuarios/' + self.uid, status=200, params=datos)

        self.assertEqual(respuesta.status_int, 200) 

    def test_parchado_usuarios_noexistente(self):
        uid = 'fitzcarraldo'
        datos = {'corpus': {'sn': 'Mendoza Castro', 'givenName': 'Anita'}}
        
        respuesta = self.testapp.patch_json('/usuarios/' + uid, status=404, params=datos)
        
        self.assertEqual(respuesta.status_int, 404)

    def test_parchado_usuarios_verificacion(self):
        datos = {'corpus': {'sn': 'Mendoza Castro', 'givenName': 'Anita'}}
        self.testapp.patch_json('/usuarios/' + self.uid, status=200, params=datos)

        respuesta = self.testapp.get('/usuarios/' + self.uid, status=200)

        self.assertEqual(respuesta.json_body['data']['sn'], datos['corpus']['sn'])

    def test_parchado_usuarios_nopermitido_clave(self):
        datos = {'corpus': {'uid': 'cambioUid'}}
        self.testapp.patch_json('/usuarios/' + self.uid, status=200, params=datos)
       
        respuesta = self.testapp.get('/usuarios/' + self.uid, status=200)

        self.assertEqual(respuesta.json_body['data']['uid'], self.uid) 

    def test_parchado_usuarios_nopermitido_clave(self):
        clave_falsa = 'espejismo'
        datos = {'corpus': {clave_falsa: 'Clave fantasmal'}}
        self.testapp.patch_json('/usuarios/' + self.uid, status=200, params=datos)
       
        respuesta = self.testapp.get('/usuarios/' + self.uid, status=200)

        self.assertFalse(clave_falsa in respuesta.json_body['data']) 
    

    def test_parchado_usuarios_agregando_clave(self):
        datos = {'corpus': {'title': 'sobrerero'}}
        self.testapp.patch_json('/usuarios/' + self.uid, status=200, params=datos)
        
        respuesta = self.testapp.get('/usuarios/' + self.uid, status=200)
        
        self.assertEqual(respuesta.json_body['data']['title'], datos['corpus']['title'])
        
