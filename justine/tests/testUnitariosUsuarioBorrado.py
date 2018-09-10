# coding: utf-8

from unittest import TestCase
from pyramid import testing
from pyramid.registry import Registry
from json import dumps

from modulosFuncionales import cargar_datos

class Borrado(TestCase):
    @classmethod
    def setUpClass(self):
        self.config = testing.setUp()
        contenido = cargar_datos()
         
        self.uid = contenido[1]['uid']
        self.datos = {"corpus": contenido[1]}
        
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
        
        self.assertEqual(respuesta['mensaje'], 'Eliminado el usuario ' + self.uid)


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

