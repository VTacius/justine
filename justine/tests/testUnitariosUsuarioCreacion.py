# coding: utf-8

from unittest import TestCase
from pyramid import testing
from pyramid.registry import Registry
from json import dumps

import logging
log = logging.getLogger('justine')

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
 
        self.assertIsInstance(respuesta, HTTPConflict)

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
        
        self.assertIsInstance(respuesta, HTTPBadRequest)

    def test_usuarios_creacion_rol_usuario(self):
        from ..views.usuarios import usuarios_creacion
        from pyramid.request import Request
        from pyramid.httpexceptions import HTTPForbidden

        datos_json = dumps(self.datos)
        
        peticion = Request.blank('', {}, body=datos_json)

        register = Registry('testing')
        peticion.registry = register
        
        jwt_claims = {'rol': 'usuario'}
        peticion.jwt_claims = jwt_claims 
        
        respuesta = usuarios_creacion(peticion)

        self.assertIsInstance(respuesta, HTTPForbidden)  
    
    def test_usuarios_creacion_rol_tecnico(self):
        from ..views.usuarios import usuarios_creacion
        from pyramid.request import Request
        from pyramid.httpexceptions import HTTPForbidden

        datos_json = dumps(self.datos)
        
        peticion = Request.blank('', {}, body=datos_json)

        register = Registry('testing')
        peticion.registry = register
        
        jwt_claims = {'rol': 'tecnicosuperior'}
        peticion.jwt_claims = jwt_claims 
        
        respuesta = usuarios_creacion(peticion)

        self.assertIsInstance(respuesta, HTTPForbidden)  
