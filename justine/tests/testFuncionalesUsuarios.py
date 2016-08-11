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
