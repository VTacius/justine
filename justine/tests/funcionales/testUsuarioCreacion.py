# coding: utf-8

from modulosFuncionales import credenciales, cargar_datos, creador_test

import logging
log = logging.getLogger('justine')

from unittest import TestCase

class Creacion(TestCase):
    @classmethod
    def setUpClass(self):
        contenido = cargar_datos('usuario')
         
        self.uid = contenido[2]['uid']
        self.datos = {"corpus": contenido[2]}

        self.token = credenciales('administrador')
        
    @classmethod
    def tearDownClass(self):
        testapp = creador_test()
        testapp.delete('/usuarios/' + self.uid, status=200, headers=self.token)

    def test_usuarios_creacion(self):

        testapp = creador_test()
        respuesta = testapp.post_json('/usuarios', status=201, params=self.datos, headers=self.token)
       
        self.assertEqual(respuesta.status_int, 201)
    
    def test_usuarios_creacion_existente(self):
        datos = self.datos
        datos['uid'] = 'alortiz'

        testapp = creador_test()
        respuesta = testapp.post_json('/usuarios', status=409, params=self.datos, headers=self.token)
        
        self.assertEqual(respuesta.status_int, 409)
    
    def test_usuarios_creacion_peticion_malformada(self):
        datos = "Mínimo esfuerzo para máximo daño"

        testapp = creador_test()
        respuesta = testapp.post_json('/usuarios', status=400, params=datos, headers=self.token)

        self.assertEqual(respuesta.status_int, 400)

    def test_usuarios_creacion_unauth(self):
        testapp = creador_test()
        respuesta = testapp.post_json('/usuarios', status=403, params=self.datos)

        self.assertRegexpMatches(str(respuesta.json_body), 'Access was denied to this resource')
