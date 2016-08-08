# coding: utf-8

from unittest import TestCase

class Listado(TestCase):
    def setUp(self):
        from justine import main
        from webtest import TestApp

        app = main({})
        self.testapp = TestApp(app)

    def test_usuarios_listado(self):
        respuesta = self.testapp.get('/usuarios', status=200, xhr=True)
        self.assertEqual(respuesta.json_body[0]['givenName'], "Rodrigo Arnoldo")

class Detalle(TestCase):
    def setUp(self):
        self.maxDiff =  None
        from justine import main
        from webtest import TestApp

        app = main({})
        self.testapp = TestApp(app)

    def test_usuarios_detalle(self):
        respuesta = self.testapp.get('/usuarios/alortiz', status=200, xhr=True)
        self.assertEqual(respuesta.json_body['data']['givenName'], 'Alexander')

    def test_usuarios_detalle_atributos(self):
        respuesta = self.testapp.get('/usuarios/alortiz', status=200, xhr=True)
        atributos = respuesta.json_body['data'].keys()
        claves = ["buzonStatus", "cuentaStatus", "dui", "fecha", "givenName", 
            "grupo", "grupos", "jvs", "loginShell", "mail", "nit", "o", "ou", 
            "pregunta", "respuesta", "sambaAcctFlags", "sn", "telephoneNumber", 
            "title", "uid", "userPassword", "usoBuzon", "volumenBuzon"]
        self.assertItemsEqual(sorted(atributos), sorted(claves))
    
    def test_usuarios_detalle_noexistente(self):
        respuesta = self.testapp.get('/usuarios/fitzcarraldo', status=404, xhr=True)
        self.assertEqual(respuesta.status_code, 404)
