# coding: utf-8

from unittest import TestCase
from pyramid import testing
from pyramid.registry import Registry
from json import dumps

from modulosFuncionales import cargar_datos

class Creacion(TestCase):
    def setUp(self):
        self.config = testing.setUp()
        contenido = cargar_datos()
         
        self.uid = contenido[1]['uid']
        self.datos = {"corpus": contenido[1]}


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
 
        self.assertEqual(respuesta['mensaje'], 'Creado el usuario ' + self.uid)

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

