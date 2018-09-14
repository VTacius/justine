# coding: utf-8

from unittest import TestCase

import logging
log = logging.getLogger('justine')

class ModelBase(TestCase):
   
    def setUp(self):
        configuracion = {
                'claves': ['givenName', 'grupo', 'grupos', 'loginShell', 'mail', 'o', 'ou', 'sambaAcctFlags', 'sn', 'telephoneNumber', 'title', 'uid', 'userPassword'],
                'traduccion' : {'title': 'jobtitle', 'sn': 'surname', 'userPassword': 'password', 'o': 'company', 'ou': 'department', 'mail': 'mailaddress', 'grupo': 'gidnumber'},
                'borrables': ['objectSid', 'objectGUID']
        }
        self.traduccion = configuracion['traduccion']
        
        self.fixture = {
            "givenName": "Olga",
            "grupo": "1005",
            "grupos": [
                "1003",
                "1005"
            ],
            "loginShell": "/bin/bash",
            "mail": "opineda@salud.gob.sv",
            "o": "1",
            "ou": "1003",
            "sn": "Pineda",
            "telephoneNumber": "7894",
            "title": "Profesor designado",
            "userPassword": "Pass_2065"
        }
       

    def test_normalizador(self):
        
        from justine.juliette.modelBase import normalizador
        
        fixture = self.fixture.copy() 
        fixture.pop('grupos', '')
        fixture.pop('sambaacctflags', '')
        fixture.pop('userPassword', '')
        
        datos = normalizador(self.traduccion, fixture)
        claves_obtenidas = datos.keys()
        claves_esperadas = ['givenname', 'gidnumber', 'loginshell', 'mailaddress', 'company', 'department', 'surname', 'telephonenumber', 'jobtitle']
       
        claves_obtenidas.sort()
        claves_esperadas.sort()

        self.assertListEqual(claves_obtenidas, claves_esperadas)
        
    def test_normalizador_utf(self):
        
        from justine.juliette.modelBase import normalizador
        
        fixture = self.fixture.copy() 
        fixture.pop('uid', '')
        fixture.pop('grupos', '')
        fixture.pop('sambaacctflags', '')
        fixture.pop('userPassword', '')
       
        # ¿Es posible usar datos con caracteres unicode
        fixture['sn'] = u"Ortíz"
        fixture['givenName'] = u"Amílcar"
        
        datos = normalizador(self.traduccion, fixture)
        claves_obtenidas = datos.keys()
        claves_esperadas = ['givenname', 'gidnumber', 'loginshell', 'mailaddress', 'company', 'department', 'surname', 'telephonenumber', 'jobtitle']
       
        claves_obtenidas.sort()
        claves_esperadas.sort()

        log.warning(claves_obtenidas)
        log.warning(claves_esperadas)
        
        self.assertListEqual(claves_obtenidas, claves_esperadas)

    def test_ldifeador(self):
        from justine.juliette.modelBase import ldifeador

        fixture = self.fixture.copy() 
        fixture.pop('uid', '')
        fixture.pop('grupos', '')
        fixture.pop('sambaacctflags', '')
        fixture.pop('userPassword', '')
        fixture['dn'] = "uid=alortiz,ou=Users,dc=salud,dc=gob,dc=sv"

        datos_nuevos = {
            "mailaddress": "fitzcarraldo@salud.gob.sv",
            "company": "Nueva localidad para usuario"
        }

        ldif = ldifeador(fixture, datos_nuevos)

        ldif_nuevo = 'dn: uid=alortiz,ou=Users,dc=salud,dc=gob,dc=sv\n'
        ldif_nuevo += 'changetype: modify\n'
        ldif_nuevo += '-\nreplace: company\n'
        ldif_nuevo += 'company: Nueva localidad para usuario\n'
        ldif_nuevo += '-\nreplace: mailaddress\n'
        ldif_nuevo += 'mailaddress: fitzcarraldo@salud.gob.sv\n'
        self.assertEqual(ldif, ldif_nuevo)
