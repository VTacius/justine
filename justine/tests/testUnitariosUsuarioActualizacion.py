# coding: utf-8

from unittest import TestCase
from pyramid import testing
from pyramid.registry import Registry
from json import dumps

from modulosFuncionales import cargar_datos

class Actualizacion(TestCase):
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
        
        register = Registry('testing')
        peticion.registry = register
        
        jwt_claims = {'rol': 'administrador'}
        peticion.jwt_claims = jwt_claims 

        respuesta = usuarios_actualizacion(peticion)
        
        self.assertEqual(respuesta['mensaje'], 'Actualizado el usuario ' + self.uid)
       
    def test_usuarios_actualizacion_peticion_malformada(self):
        pass
        #from ..views.usuarios import usuarios_actualizacion
        #from pyramid.request import Request
        #from pyramid.httpexceptions import HTTPBadRequest

        #datos = 'Maximo daño con el mínimo esfuerzo'
        #peticion = Request.blank('', {}, body = datos)
        #peticion.matchdict = {'usuario': self.uid}
        #
        #register = Registry('testing')
        #peticion.registry = register
        #
        #respuesta = usuarios_actualizacion(peticion)
        #
        #self.assertEqual(type(respuesta), HTTPBadRequest)

    def test_usuarios_actualizacion_noexistente(self):
        from ..views.usuarios import usuarios_actualizacion
        from pyramid.request import Request
        from pyramid.httpexceptions import HTTPNotFound
        
        uid = 'fitzcarraldo'
        datos = dumps({'corpus': {'uid': uid, 'sn':'Mendoza', 'givenName': 'Ana'}})
        
        peticion = Request.blank('', {}, body=datos)
        peticion.matchdict = {'usuario': uid}
        
        register = Registry('testing')
        peticion.registry = register
        
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

        register = Registry('testing')
        peticion.registry = register
        
        respuesta = usuarios_actualizacion(peticion)

        self.assertEqual(type(respuesta), HTTPBadRequest)

        

