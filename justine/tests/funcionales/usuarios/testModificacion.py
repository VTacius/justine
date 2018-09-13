# coding: utf-8

from unittest import TestCase
from ..modulos import cargar_datos, cargar_credenciales

import logging
log = logging.getLogger('justine')

class Modificacion(TestCase):
    """
    NOTA: Sobre la validación de datos, testar directamente nuestra pequeña clase 
    TODO: Validar cambio de grupo principal
    TODO: Validar cambio de estado de la cuenta
    TODO: Validar cambios de grupos
    TODO: Validar cambio de contraseña
    TODO: Validar que tan pocas claves podemos cambiar
    """

    @classmethod
    def setUpClass(self):

        # Cargamos los datos
        entidad = cargar_datos('usuario')[2]
        self.uid = entidad['uid']
        self.datos = {'corpus': entidad}

        # Trabajamos en obtener un token
        self.token = cargar_credenciales()
        
        # Creamos nuestro objeto para pruebas
        from justine import main
        from webtest import TestApp

        app = main({})
        self.testapp = TestApp(app)

        res = self.testapp.post_json('/usuarios', status=201, params=self.datos, headers=self.token)

    @classmethod
    def tearDownClass(self):
        res = self.testapp.head('/usuarios/' + self.uid, status="*", headers=self.token)
        if res.status_int == 200:
            self.testapp.delete('/usuarios/' + self.uid, status=200, headers=self.token)

    def test_actualizacion(self):
        self.datos['corpus']['title'] = "Titulador"
        
        self.testapp.patch_json('/usuarios/' + self.uid, status=200, params=self.datos, headers=self.token)
        
        res = self.testapp.get('/usuarios/' + self.uid, status=200, headers=self.token)
        respuesta = res.json_body['mensaje'][0]['title']
        datos = self.datos['corpus']['title']
        
        self.assertEqual(respuesta, datos)

    def test_actualizacion_displayName(self):
        sn = "Sotomayor"
        givenName = self.datos['corpus']['givenName']
        displayName = givenName + " " + sn 
        
        self.datos['corpus']['sn'] = sn
        self.testapp.patch_json('/usuarios/' + self.uid, status=200, params=self.datos, headers=self.token)
        
        res = self.testapp.get('/usuarios/' + self.uid, status=200, headers=self.token)
        respuesta = res.json_body['mensaje'][0]['displayName']
        
        self.assertEqual(respuesta, displayName)

    def test_corpus_faltante(self):
        datos = {'cuerpo': self.datos['corpus'].copy()}
        
        self.testapp.patch_json('/usuarios/' + self.uid, status=400, params=datos, headers=self.token)
    
    def test_json_malformateado(self):
        datos = "Mínimo esfuerzo para máximo daño"
        self.testapp.patch_json('/usuarios/' + self.uid, status=400, params=datos, headers=self.token)
    
    def test_noexistente(self):
        uid = 'fitzcarraldo'
        datos = {'corpus': self.datos['corpus'].copy()}
        datos['corpus']['uid'] = uid
        
        self.testapp.patch_json('/usuarios/' + uid, status=404, params=datos, headers=self.token)

    def test_claves_incompletas(self):
        cuerpo = self.datos['corpus'].copy()
        del cuerpo['sn']
        del cuerpo['givenName']
        datos = {'corpus': cuerpo}
        
        self.testapp.patch_json('/usuarios/' + self.uid, status=200, params=datos, headers=self.token)

    def test_actualizacion_noauth(self):
        self.testapp.patch_json('/usuarios/' + self.uid, status=403, params=self.datos)
        
