# coding: utf-8

from modulosFuncionales import credenciales

import logging
log = logging.getLogger('justine')

from unittest import TestCase

class Detalle(TestCase):

    def setUp(self):
        self.maxDiff =  None
        from justine import main
        from webtest import TestApp

        app = main({})
        self.testapp = TestApp(app)

        # Obtenemos un token con credenciales de administrador 
        self.token = credenciales('administrador')
        
        self.claves_administrador = ["buzonStatus", "cuentaStatus", "dui", "fecha", "givenName", 
            "grupo", "grupos", "loginShell", "mail", "nit", "o", "ou", 
            "pregunta", "respuesta", "sambaAcctFlags", "sn", "telephoneNumber", 
            "title", "uid", "userPassword", "usoBuzon", "volumenBuzon"]
        self.claves_tecnico = ['buzonStatus', 'cuentaStatus', 'givenName', 'grupo', 'grupos', 'loginShell', 'mail', 'o', 
            'ou', 'sambaAcctFlags', 'sn', 'telephoneNumber', 'title', 'uid', 'userPassword', 'usoBuzon', 'volumenBuzon']
        
    def test_usuarios_detalle(self):
        respuesta = self.testapp.get('/usuarios/alortiz', status=200, xhr=True, headers=self.token)

        self.assertEqual(respuesta.json_body['mensaje'][0]['cn'], 'alortiz')
    
    def test_usuarios_detalle_noexistente(self):
        uid = 'fitzcarraldo'
        
        respuesta = self.testapp.get('/usuarios/' + uid, status=404, xhr=True, headers=self.token)

        self.assertEqual(respuesta.status_code, 404)

    ## TODO: Deberías comprobar como es que realmente nos vamos a comportar respecto a este apartado
    #def test_usuarios_detalle_atributos(self):
    #    respuesta = self.testapp.get('/usuarios/alortiz', status=200, xhr=True, headers=self.token)
    #    atributos = respuesta.json_body['mensaje'][0].keys()
    #    self.assertItemsEqual(sorted(atributos), sorted(self.claves_administrador))

    def test_usuarios_detalle_unauth(self):
        respuesta = self.testapp.get('/usuarios/alortiz', status=403, xhr=True)
        
        self.assertRegexpMatches(respuesta.body, 'Access was denied to this resource')

