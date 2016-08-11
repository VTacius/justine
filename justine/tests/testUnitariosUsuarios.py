# coding: utf-8

from unittest import TestCase
from pyramid import testing
from json import dumps

class Listado(TestCase):
    def setUp(self):
        self.maxDiff =  None
        self.config = testing.setUp()

    def tearDown(self):
        self.config = testing.tearDown()

    def test_usuarios_listado(self):
        from ..views.usuarios import usuarios_listado
        peticion = testing.DummyRequest()
        respuesta = usuarios_listado(peticion)
        self.assertEqual(respuesta[0]['givenName'], "Rodrigo Arnoldo")
    
    def test_usuarios_listado_contador(self):
        from ..views.usuarios import usuarios_listado
        peticion = testing.DummyRequest()
        respuesta = usuarios_listado(peticion)
        self.assertTrue(len(respuesta) <= 250)

class Detalle(TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        self.config = testing.tearDown()

    def test_usuarios_detalle(self):
        from ..views.usuarios import usuarios_detalle
        peticion = testing.DummyRequest
        peticion.matchdict = {'usuario': 'alortiz'}
        respuesta = usuarios_detalle(peticion)
        self.assertEqual(respuesta['data']['givenName'], 'Alexander')

    def test_usuarios_detalle_contador(self):
        from ..views.usuarios import usuarios_detalle
        peticion = testing.DummyRequest
        peticion.matchdict = {'usuario': 'alortiz'}
        respuesta = usuarios_detalle(peticion)
        self.assertTrue('data' in respuesta)

class Creacion(TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.uid = "alortiz"
        self.datos = {"corpus": {"uid": self.uid, "sambaAcctFlags": True, "dui": "123456789-0", "title": "Gerente de Oficina", 
            "grupos": ["1003", "1039", "1034"], "usoBuzon": "150MB", "fecha": "01/11/1980", "mail": "opineda@salud.gob.sv", 
            "respuesta": "La misma de siempre", "loginShell": "false", "pregunta": "¿Cuál es mi pregunta?", "buzonStatus": True, 
            "grupo": "512", "nit": "4654-456546-142-3", "telephoneNumber": "7459", "cuentaStatus": True, "volumenBuzon": "500MB", 
            "o": {"nombre": "Secretaría de Estado SS Ministerio de Salud", "id": 1038}, "jvs": {"estado": True, "valor": None}, 
            "sn": "Quintanilla", "ou": "Unidad Financiera Institucional", "givenName": "Elida", "userPassword": "Abc_9999"}}

    def tearDown(self):
        self.config = testing.tearDown()
    
    """ 
    Sigo sin ser capaz de crear el usuarios, el método debería ser este sin mayores inconvenientes
    El problema consiste en que esta peticion carece del atributo registry, que sigo sin entender de donde lo saca, 
    pero que lo hecha de menos cuando hago request.response en la vista 
    
    """
    #def test_usuarios_creacion(self):
    #    from ..views.usuarios import usuarios_creacion
    #    from pyramid.request import Request
 
    #    datos = dumps(self.datos)
    #    peticion = Request.blank('', {}, body=datos)

    #    respuesta = usuarios_creacion(peticion)
 
    #    self.assertEqual(respuesta, 'http://localhost/usuarios/' + self.uid)

    def test_usuarios_creacion_existente(self):
        from ..views.usuarios import usuarios_creacion
        from pyramid.request import Request
        from pyramid.httpexceptions import HTTPConflict
        
        datos = self.datos
        datos['corpus']['uid'] = 'alortiz'       
        datos_json = dumps(datos) 
       
        peticion = Request.blank('', {}, body=datos_json)

        respuesta = usuarios_creacion(peticion)
 
        self.assertEqual(type(respuesta) , HTTPConflict)

    def test_usuarios_creacion_peticion_malformada(self):
        from ..views.usuarios import usuarios_creacion
        from pyramid.request import Request
        from pyramid.httpexceptions import HTTPBadRequest

        datos = 'Maximo daño con el mínimo esfuerzo'

        peticion = Request.blank('', {}, body=datos)
        
        respuesta = usuarios_creacion(peticion)
        
        self.assertTrue(isinstance(respuesta, HTTPBadRequest))

class Borrado(TestCase):
    @classmethod
    def setUpClass(self):
        self.config = testing.setUp()
        self.uid = "lmulato"
        self.datos = {"corpus": {"uid": self.uid, "sambaAcctFlags": True, "dui": "123456789-0", "title": "Gerente de Oficina", 
            "grupos": ["1003", "1039", "1034"], "usoBuzon": "150MB", "fecha": "01/11/1980", "mail": "opineda@salud.gob.sv", 
            "respuesta": "La misma de siempre", "loginShell": "false", "pregunta": "¿Cuál es mi pregunta?", "buzonStatus": True, 
            "grupo": "512", "nit": "4654-456546-142-3", "telephoneNumber": "7459", "cuentaStatus": True, "volumenBuzon": "500MB", 
            "o": {"nombre": "Secretaría de Estado SS Ministerio de Salud", "id": 1038}, "jvs": {"estado": True, "valor": None}, 
            "sn": "Mulato", "ou": "Unidad Financiera Institucional", "givenName": "Lorena", "userPassword": "Abc_9999"}}
        
        # Creo que esto es de lo peor que puedo hacer: Usar métodos más funcionales que unitarios
        # en un test unitario, sin embargo es la única forma de sobrepasar el problema

        from justine import main        
        from webtest import TestApp

        app = main({})
        testapp = TestApp(app)
        
        testapp.post_json('/usuarios', status=201, params=self.datos)  

    @classmethod
    def tearDownClass(self):
        self.config = testing.tearDown()

    def test_usuarios_borrado(self):
        from ..views.usuarios import usuarios_borrado
        
        peticion = testing.DummyRequest()
        peticion.matchdict = {'usuario': self.uid}
        
        respuesta = usuarios_borrado(peticion)
        
        self.assertEqual(respuesta['mensaje'], self.uid + " Borrado")


    def test_usuarios_borrado_inexistente(self):
        from ..views.usuarios import usuarios_borrado
        from pyramid.httpexceptions import HTTPNotFound
        
        uid = "fitzcarraldo"    
            
        peticion = testing.DummyRequest()
        peticion. matchdict = {'usuario': uid}

        respuesta = usuarios_borrado(peticion)

        self.assertEqual(type(respuesta), HTTPNotFound)

