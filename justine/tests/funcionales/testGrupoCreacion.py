# coding: utf-8

from modulosFuncionales import credenciales, cargar_datos, creador_test

import logging
log = logging.getLogger('justine')

from unittest import TestCase

class Creacion(TestCase):
    @classmethod
    def setUpClass(self):
        contenido = cargar_datos('grupo')
         
        self.cn = contenido[0]['cn']
        self.datos = {"corpus": contenido[0]}

        self.token = credenciales('administrador')
        
    @classmethod
    def tearDownClass(self):
        testapp = creador_test()
        testapp.delete('/grupos/' + self.cn, status=200, headers=self.token)
    
    def test_usuarios_creacion(self):

        testapp = creador_test()
        respuesta = testapp.post_json('/grupos', status=201, params=self.datos, headers=self.token)
       
        self.assertEqual(respuesta.status_int, 201)
