# coding: utf-8

from modulosFuncionales import credenciales, cargar_datos, creador_test

from unittest import TestCase

# TODO: Tení que trabajar sobre los siguiente casos:
## TODO: Datos incorrectos: Tipo enteros sobre todo
## TODO: Datos incorrectos: Claves que no pertenecen al esquema
## TODO: Datos incorrectos: uid en la URL no coincide co la url de los datos
## TODO: gidNumber equivocado

class Actualizacion(TestCase):

    @classmethod
    def setUpClass(self):
        contenido = cargar_datos('usuario')
        
        self.uid = contenido[0]['uid']
        self.datos = {"corpus": contenido[0]}
        self.token = credenciales('administrador') 
      
        testapp = creador_test()

        # Creamos un usuario totalmente diferente a todo lo creado, estoy casi seguro que esta parte si debe funcionar de esta forma
        testapp.post_json('/usuarios', status=201, params=self.datos, headers=self.token)
    
    @classmethod
    def tearDownClass(self):
        testapp = creador_test()
        testapp.delete('/usuarios/' + self.uid, status=200, headers=self.token)   
     
    def test_usuarios_actualizacion(self):
        datos = self.datos
        datos['corpus']['givenName'] = 'Claudia Carolina'
        datos['corpus']['sn'] = 'Peña Nieto'

        testapp = creador_test()
        respuesta = testapp.put_json('/usuarios/' + self.uid, status=200, params=datos, headers=self.token)

        self.assertEqual(respuesta.status_int, 200)

    def test_usuarios_actualizacion_noexistente(self):
        datos = dict(self.datos)
        uid = datos['corpus']['uid'] = 'fitzcarraldo'

        testapp = creador_test()
        respuesta = testapp.put_json('/usuarios/' + uid, status=404, params=datos, headers=self.token)
    
        self.assertEqual(respuesta.status_int, 404)
    
    def test_usuarios_actualizacion_uid_nocoincidente(self):
        datos = self.datos
        datos['corpus']['uid'] = 'fitzcarraldo' 

        testapp = creador_test()
        respuesta = testapp.put_json('/usuarios/' + self.uid, status=400, params=datos, headers=self.token)
        
        self.assertEqual(respuesta.status_int, 400)
    
    def test_usuarios_actualizacion_uid_peticion_malformada(self):
        datos = 'Mínimo esfuerzo para máximo daño'

        testapp = creador_test()
        respuesta = testapp.put_json('/usuarios/' + self.uid, status=400, params=datos, headers=self.token)

        self.assertEqual(respuesta.status_int, 400)

    def test_usuarios_actualizacion_claves_incompletas(self):
        sn = 'Castro Ortega'
        datos = {'corpus': {'uid': self.uid, 'sn': sn}}

        testapp = creador_test()
        respuesta = testapp.put_json('/usuarios/' + self.uid, status=400, params=datos, headers=self.token)

    def test_usuarios_actualizacion_unauth(self):
        self.datos['corpus']['uid'] = self.uid
        
        testapp = creador_test()
        respuesta = testapp.put_json('/usuarios/' + self.uid, status=403, params=self.datos)

        self.assertRegexpMatches(str(respuesta.json_body), 'Access was denied to this resource')
    
    def test_usuarios_actualizacion_rol_tecnico(self):
        self.datos['corpus']['uid'] = self.uid
        
        testapp = creador_test()
        respuesta = testapp.put_json('/usuarios/' + self.uid, status=403, params=self.datos)

        self.assertRegexpMatches(str(respuesta.json_body), 'Access was denied to this resource')
    
    def test_usuarios_actualizacion_rol_usuario(self):
        self.datos['corpus']['uid'] = self.uid
        
        testapp = creador_test()
        respuesta = testapp.put_json('/usuarios/' + self.uid, status=403, params=self.datos)

        self.assertRegexpMatches(str(respuesta.json_body), 'Access was denied to this resource')
