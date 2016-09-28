# coding: utf-8

from unittest import TestCase
from pyramid import testing
from pyramid.registry import Registry
from json import dumps

import logging
log = logging.getLogger('justine')

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

    def test_usuarios_borrado_rol_tecnico(self):
        from ..views.usuarios import usuarios_borrado
        from pyramid.httpexceptions import HTTPForbidden
        
        peticion = testing.DummyRequest()
        peticion.matchdict = {'usuario': self.uid}

        jwt_claims = {'rol': 'tecnicosuperior'}
        peticion.jwt_claims = jwt_claims
        
        respuesta = usuarios_borrado(peticion)
        self.assertIsInstance(respuesta, HTTPForbidden)
