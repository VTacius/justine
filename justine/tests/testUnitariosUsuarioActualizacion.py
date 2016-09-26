# coding: utf-8

from unittest import TestCase
from pyramid import testing
from pyramid.registry import Registry
from json import dumps

import logging
log = logging.getLogger('justine')

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
        

