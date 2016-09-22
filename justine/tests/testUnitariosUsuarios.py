# coding: utf-8

from unittest import TestCase
from pyramid import testing
from pyramid.registry import Registry
from webob.multidict import MultiDict
from json import dumps

import logging
log = logging.getLogger('justine')

class Listado(TestCase):
    def setUp(self):
        self.maxDiff =  None
        self.config = testing.setUp()

    def tearDown(self):
        self.config = testing.tearDown()

    def test_usuarios_listado(self):
        from ..views.usuarios import usuarios_listado
        from pyramid.request import Request

        peticion = Request.blank('', {})
        
        register = Registry('testing')
        peticion.register = register

        jwt_claims = {'rol': 'administrador'}
        peticion.jwt_claims = jwt_claims 

        respuesta = usuarios_listado(peticion)
        
        self.assertEqual(respuesta[0]['givenName'], "Baloncesto")
    
    def test_usuarios_listado_contador(self):
        from ..views.usuarios import usuarios_listado
        from pyramid.request import Request

        peticion = Request.blank('', {})

        register = Registry('testing')
        peticion.register = register
        
        jwt_claims = {'rol': 'administrador'}
        peticion.jwt_claims = jwt_claims 

        respuesta = usuarios_listado(peticion)
        self.assertTrue(len(respuesta) <= 250)

class Detalle(TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        self.config = testing.tearDown()

    def test_usuarios_detalle(self):
        from ..views.usuarios import usuarios_detalle
        from pyramid.request import Request
        
        peticion = Request.blank('', {})
        peticion.matchdict = {'usuario': 'alortiz'}
        
        register = Registry('testing')
        peticion.registry = register
        
        jwt_claims = {'rol': 'administrador'}
        peticion.jwt_claims = jwt_claims 

        respuesta = usuarios_detalle(peticion)
        self.assertEqual(respuesta['mensaje']['givenName'], 'Alexander')

    def test_usuarios_detalle_contador(self):
        from ..views.usuarios import usuarios_detalle
        peticion = testing.DummyRequest
        
        jwt_claims = {'rol': 'administrador'}
        peticion.jwt_claims = jwt_claims 
        
        peticion.matchdict = {'usuario': 'alortiz'}
        respuesta = usuarios_detalle(peticion)
        self.assertTrue('mensaje' in respuesta)

class Creacion(TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.uid = "tcalcuta"
        self.datos = {"corpus": {"uid": self.uid, "sambaAcctFlags": True, "dui": "123456789-0", "title": "Gerente de Oficina", 
            "grupos": [1003, 1039, 1034], "usoBuzon": 150, "fecha": "1980-11-02", "mail": "opineda@salud.gob.sv", 
            "respuesta": "La misma de siempre", "loginShell": "false", "pregunta": "¿Cuál es mi pregunta?", "buzonStatus": True, 
            "grupo": 512, "nit": "4654-456546-142-3", "telephoneNumber": "7459", "cuentaStatus": True, "volumenBuzon": 500, 
            "o": {"nombre": "Secretaría de Estado SS Ministerio de Salud", "id": 1038}, "jvs": {"estado": False, "valor": None}, 
            "sn": "Quintanilla", "ou": "Unidad Financiera Institucional", "givenName": "Elida", "userPassword": "Abc_9999"}}

    def tearDown(self):
        from ..views.usuarios import usuarios_borrado
        self.config = testing.tearDown()
        
        peticion = testing.DummyRequest()
        peticion.matchdict = {'usuario': self.uid}
        
        jwt_claims = {'rol': 'administrador'}
        peticion.jwt_claims = jwt_claims 


        usuarios_borrado(peticion)
    
    def test_usuarios_creacion(self):
        from ..views.usuarios import usuarios_creacion
        from pyramid.request import Request
 
        datos = dumps(self.datos)
        peticion = Request.blank('', {}, body=datos)

        register = Registry('testing')
        peticion.registry = register

        jwt_claims = {'rol': 'administrador'}
        peticion.jwt_claims = jwt_claims 

        respuesta = usuarios_creacion(peticion)
 
        self.assertEqual(respuesta['mensaje'], '/usuarios/' + self.uid)

    def test_usuarios_creacion_existente(self):
        from ..views.usuarios import usuarios_creacion
        from pyramid.request import Request
        from pyramid.httpexceptions import HTTPConflict
        
        datos = self.datos
        datos['corpus']['uid'] = 'alortiz'       
        datos_json = dumps(datos) 
       
        peticion = Request.blank('', {}, body=datos_json)
        
        register = Registry('testing')
        peticion.registry = register

        jwt_claims = {'rol': 'administrador'}
        peticion.jwt_claims = jwt_claims 

        respuesta = usuarios_creacion(peticion)
 
        self.assertEqual(type(respuesta), HTTPConflict)

    def test_usuarios_creacion_peticion_malformada(self):
        from ..views.usuarios import usuarios_creacion
        from pyramid.request import Request
        from pyramid.httpexceptions import HTTPBadRequest

        datos = 'Maximo daño con el mínimo esfuerzo'

        peticion = Request.blank('', {}, body=datos)
        
        register = Registry('testing')
        peticion.registry = register
        
        jwt_claims = {'rol': 'administrador'}
        peticion.jwt_claims = jwt_claims 

        respuesta = usuarios_creacion(peticion)
        
        self.assertTrue(isinstance(respuesta, HTTPBadRequest))

class Borrado(TestCase):
    @classmethod
    def setUpClass(self):
        self.config = testing.setUp()
        self.uid = "lmulato"
        self.datos = {"corpus": {"uid": self.uid, "sambaAcctFlags": True, "dui": "123456789-0", "title": "Gerente de Oficina", 
            "grupos": [1003, 1039, 1034], "usoBuzon": 150, "fecha": "1980-11-02", "mail": "opineda@salud.gob.sv", 
            "respuesta": "La misma de siempre", "loginShell": "false", "pregunta": "¿Cuál es mi pregunta?", "buzonStatus": True, 
            "grupo": 512, "nit": "4654-456546-142-3", "telephoneNumber": "7459", "cuentaStatus": True, "volumenBuzon": 500, 
            "o": {"nombre": "Secretaría de Estado SS Ministerio de Salud", "id": 1038}, "jvs": {"estado": False, "valor": None}, 
            "sn": "Mulato", "ou": "Unidad Financiera Institucional", "givenName": "Lorena", "userPassword": "Abc_9999"}}
        
        from ..views.usuarios import usuarios_creacion
        from pyramid.request import Request
 
        datos = dumps(self.datos)
        peticion = Request.blank('', {}, body=datos)

        register = Registry('testing')
        peticion.registry = register

        jwt_claims = {'rol': 'administrador'}
        peticion.jwt_claims = jwt_claims 

        respuesta = usuarios_creacion(peticion)

    @classmethod
    def tearDownClass(self):
        self.config = testing.tearDown()

    def test_usuarios_borrado(self):
        from ..views.usuarios import usuarios_borrado
        
        peticion = testing.DummyRequest()
        peticion.matchdict = {'usuario': self.uid}
        
        jwt_claims = {'rol': 'administrador'}
        peticion.jwt_claims = jwt_claims 

        respuesta = usuarios_borrado(peticion)
        
        self.assertEqual(respuesta['mensaje'], self.uid + " Borrado")


    def test_usuarios_borrado_inexistente(self):
        from ..views.usuarios import usuarios_borrado
        from pyramid.httpexceptions import HTTPNotFound
        
        uid = "fitzcarraldo"    
            
        peticion = testing.DummyRequest()
        peticion. matchdict = {'usuario': uid}

        jwt_claims = {'rol': 'administrador'}
        peticion.jwt_claims = jwt_claims 

        respuesta = usuarios_borrado(peticion)

        self.assertEqual(type(respuesta), HTTPNotFound)

class Actualizacion(TestCase):
    @classmethod
    def setUpClass(self):
        
        self.config = testing.setUp()
        self.uid = "lmulato"
        self.datos = {"corpus": {"uid": self.uid, "sambaAcctFlags": True, "dui": "123456789-0", "title": "Gerente de Oficina", 
            "grupos": [1003, 1039, 1034], "usoBuzon": 150, "fecha": "1980-11-02", "mail": "opineda@salud.gob.sv", 
            "respuesta": "La misma de siempre", "loginShell": "false", "pregunta": "¿Cuál es mi pregunta?", "buzonStatus": True, 
            "grupo": 512, "nit": "4654-456546-142-3", "telephoneNumber": "7459", "cuentaStatus": True, "volumenBuzon": 500, 
            "o": {"nombre": "Secretaría de Estado SS Ministerio de Salud", "id": 1038}, "jvs": {"estado": False, "valor": None}, 
            "sn": "Mulato", "ou": "Unidad Financiera Institucional", "givenName": "Lorena", "userPassword": "Abc_9999"}}
        
        from ..views.usuarios import usuarios_creacion
        from pyramid.request import Request
 
        datos = dumps(self.datos)
        peticion = Request.blank('', {}, body=datos)

        register = Registry('testing')
        peticion.registry = register

        jwt_claims = {'rol': 'administrador'}
        peticion.jwt_claims = jwt_claims 

        respuesta = usuarios_creacion(peticion)

    @classmethod
    def tearDownClass(self):
        self.config = testing.tearDown()
        from ..views.usuarios import usuarios_borrado
        
        peticion = testing.DummyRequest()
        peticion.matchdict = {'usuario': self.uid}

        usuarios_borrado(peticion)
    
    def test_usuarios_actualizacion(self):
        from ..views.usuarios import usuarios_actualizacion
        from pyramid.request import Request
        data = self.datos
        data['corpus']['sn'] = 'Mendoza'
        data['corpus']['givenName'] = 'Ana'
        datos = dumps(data)
 
        peticion = Request.blank('', {}, body = datos)
        peticion.matchdict = {'usuario': self.uid}
        
        jwt_claims = {'rol': 'administrador'}
        peticion.jwt_claims = jwt_claims 

        respuesta = usuarios_actualizacion(peticion)
        
        self.assertEqual(respuesta['mensaje'], self.uid + ' Actualizado')
       
    def test_usuarios_actualizacion_peticion_malformada(self):
        from ..views.usuarios import usuarios_actualizacion
        from pyramid.request import Request
        from pyramid.httpexceptions import HTTPBadRequest

        datos = 'Maximo daño con el mínimo esfuerzo'
        peticion = Request.blank('', {}, body = datos)
        peticion.matchdict = {'usuario': self.uid}
        
        respuesta = usuarios_actualizacion(peticion)
        
        self.assertEqual(type(respuesta), HTTPBadRequest)

    def test_usuarios_actualizacion_noexistente(self):
        from ..views.usuarios import usuarios_actualizacion
        from pyramid.request import Request
        from pyramid.httpexceptions import HTTPNotFound
        
        uid = 'fitzcarraldo'
        datos = dumps({'corpus': {'uid': uid, 'sn':'Mendoza', 'givenName': 'Ana'}})
        
        peticion = Request.blank('', {}, body=datos)
        peticion.matchdict = {'usuario': uid}
        
        jwt_claims = {'rol': 'administrador'}
        peticion.jwt_claims = jwt_claims 

        respuesta = usuarios_actualizacion(peticion)
        
        self.assertEqual(type(respuesta), HTTPNotFound)

    def test_usuarios_actualizacion_no_correlacion(self):
        from ..views.usuarios import usuarios_actualizacion
        from pyramid.request import Request
        from pyramid.httpexceptions import HTTPBadRequest

        uid_principal = 'alortiz'
        uid_alterno = 'fitzcarraldo'
        datos = dumps({'corpus': {'uid': uid_principal, 'sn':'Mendoza', 'givenName': 'Ana'}})
        
        peticion = Request.blank('', {}, body=datos)
        peticion.matchdict = {'usuario': uid_alterno}

        respuesta = usuarios_actualizacion(peticion)

        self.assertEqual(type(respuesta), HTTPBadRequest)

    def test_usuarios_actualizacion_claves_completas(self):
        from ..views.usuarios import usuarios_actualizacion
        from ..views.usuarios import usuarios_detalle
        from pyramid.request import Request

        uid = 'alortiz'
        sn = 'Castro Ortega'
        datos = dumps({'corpus': {'uid': uid, 'sn': sn}})
        peticion = Request.blank('', {}, body=datos)
        peticion.matchdict = {'usuario': uid}

        respuesta = usuarios_actualizacion(peticion)

        peticion = testing.DummyRequest()
        peticion.matchdict = {'usuario': uid}

        jwt_claims = {'rol': 'administrador'}
        peticion.jwt_claims = jwt_claims 

        respuesta = usuarios_detalle(peticion)

        self.assertEqual(respuesta['mensaje']['sn'], sn)
        
class Modificacion(TestCase):
    @classmethod
    def setUpClass(self):
        self.config = testing.setUp()
        self.uid = 'jabdalah'
        self.datos = {'corpus': {'uid': self.uid, 'sn':'Mendoza', 'givenName': 'Ana', "o": {"nombre": "Secretaría de Estado SS Ministerio de Salud", "id": 1038}}}
      
        from ..views.usuarios import usuarios_creacion
        from pyramid.request import Request
 
        datos = dumps(self.datos)
        peticion = Request.blank('', {}, body=datos)

        register = Registry('testing')
        peticion.registry = register

        jwt_claims = {'rol': 'administrador'}
        peticion.jwt_claims = jwt_claims 

        respuesta = usuarios_creacion(peticion)

    @classmethod
    def tearDownClass(self):
        from ..views.usuarios import usuarios_borrado
        
        peticion = testing.DummyRequest()
        peticion.matchdict = {'usuario': self.uid}

        jwt_claims = {'rol': 'administrador'}
        peticion.jwt_claims = jwt_claims 

        usuarios_borrado(peticion)

    def test_usuarios_modificacion(self):
        from ..views.usuarios import usuarios_modificacion
        from pyramid.request import Request

        datos = {'corpus': {'uid': self.uid, 'sn': 'Mendoza Castro', 'givenName': 'Anita'}}
        datos_json = dumps(datos)
        
        peticion = Request.blank('', {}, body=datos_json)
        peticion.matchdict = {'usuario': self.uid}

        jwt_claims = {'rol': 'administrador'}
        peticion.jwt_claims = jwt_claims 

        respuesta = usuarios_modificacion(peticion)
        self.assertEqual(respuesta['mensaje'], self.uid + " Parchado")

    def test_usuarios_modificacion_noexistente(self):
        from ..views.usuarios import usuarios_modificacion
        from pyramid.request import Request
        from pyramid.httpexceptions import HTTPNotFound
        
        data = self.datos
        
        uid = 'fitzcarraldo'        
        data['corpus']['uid'] = uid 
        data['corpus']['sn'] = 'Mendoza Castro'
        data['corpus']['givenName'] = 'Anita'
        datos = dumps(data)
        
        peticion =  Request.blank('', {}, body = datos)
        peticion.matchdict = {'usuario': uid}

        jwt_claims = {'rol': 'administrador'}
        peticion.jwt_claims = jwt_claims 

        respuesta = usuarios_modificacion(peticion)
        
        self.assertEqual(type(respuesta), HTTPNotFound)

    def test_usuarios_modificacion_peticion_malformada(self):
        from ..views.usuarios import usuarios_modificacion
        from pyramid.request import Request
        from pyramid.httpexceptions import HTTPBadRequest

        datos = 'Maximo daño con el mínimo esfuerzo'

        peticion = Request.blank('', {}, body=datos)
        peticion.matchdict = {'usuario': self.uid}
        
        respuesta = usuarios_modificacion(peticion)

        self.assertEqual(type(respuesta),  HTTPBadRequest)
