# coding: utf-8

from unittest import TestCase
from pyramid import testing
from pyramid.registry import Registry
from json import dumps

from modulosFuncionales import cargar_datos

class Modificacion(TestCase):

    @classmethod
    def setUpClass(self):
        self.config = testing.setUp()
        contenido = cargar_datos('usuario')
         
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

        register = Registry('testing')
        peticion.registry = register

        jwt_claims = {'rol': 'administrador'}
        peticion.jwt_claims = jwt_claims 

        respuesta = usuarios_modificacion(peticion)
        self.assertEqual(respuesta['mensaje'], "Actualizado el usuario " + self.uid)

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

        register = Registry('testing')
        peticion.registry = register

        jwt_claims = {'rol': 'administrador'}
        peticion.jwt_claims = jwt_claims 

        respuesta = usuarios_modificacion(peticion)
        
        self.assertEqual(type(respuesta), HTTPNotFound)

    def test_usuarios_modificacion_peticion_malformada(self):
        pass
        #from ..views.usuarios import usuarios_modificacion
        #from pyramid.request import Request
        #from pyramid.httpexceptions import HTTPBadRequest

        #datos = 'Maximo daño con el mínimo esfuerzo'

        #peticion = Request.blank('', {}, body=datos)
        #peticion.matchdict = {'usuario': self.uid}
        #
        #register = Registry('testing')
        #peticion.registry = register

        #respuesta = usuarios_modificacion(peticion)

        #self.assertEqual(type(respuesta),  HTTPBadRequest)
