# coding: utf-8

from modulosFuncionales import credenciales, cargar_datos, creador_test

import logging
log = logging.getLogger('justine')

from unittest import TestCase

class Borrado(TestCase):  

    @classmethod
    def setUpClass(self):
        contenido = cargar_datos('usuario')
         
        self.uid = contenido[1]['uid']
        self.datos = {"corpus": contenido[1]}
        
        self.token = credenciales('administrador')

        testapp = creador_test()
        # Creamos un usuarios que luego vamos a borrar, al menos un mi mente así funciona estas cosas
        testapp.post_json('/usuarios', status=201, params=self.datos, headers=self.token)
    
    def test_usuarios_borrado(self):
        testapp = creador_test()
        respuesta = testapp.delete('/usuarios/' + self.uid, status=200, headers=self.token)

        self.assertEqual(respuesta.status_int, 200)
    
    def test_usuarios_borrado_inexistente(self):
        uid = "fitzcarraldo"

        testapp = creador_test()
        respuesta = testapp.delete('/usuarios/' + uid, status=404, headers=self.token)

        self.assertEqual(respuesta.status_int, 404)

    def test_usuarios_borrado_unauth(self):
        testapp = creador_test()
        respuesta = testapp.delete('/usuarios/' + self.uid, status=403)
        
        self.assertRegexpMatches(str(respuesta.json_body), 'Access was denied to this resource')


















