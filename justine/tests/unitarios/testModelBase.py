# coding: utf-8

from unittest import TestCase

import logging
log = logging.getLogger('justine')

class ModelBase(TestCase):
    
    def test_normalizador(self):
        configuracion = {
                'claves': ['givenName', 'grupo', 'grupos', 'loginShell', 'mail', 'o', 'ou', 'sambaAcctFlags', 'sn', 'telephoneNumber', 'title', 'uid', 'userPassword'],
                'traduccion' : {'title': 'jobtitle', 'sn': 'surname', 'userPassword': 'password', 'o': 'company', 'ou': 'department', 'mail': 'mailaddress', 'grupo': 'gidnumber'},
                'borrables': ['objectSid', 'objectGUID']
        }
        
        from justine.juliette.modelBase import normalizador
        
        fixture = {
            "givenName": "Olga",
            "grupo": "1005",
            "loginShell": "/bin/bash",
            "mail": "opineda@salud.gob.sv",
            "o": "1",
            "ou": "1003",
            "sn": "Pineda",
            "telephoneNumber": "7894",
            "title": "Profesor designado",
            "uid": "opineda",
            "userPassword": "Pass_2065"
        }
       
        
        datos = normalizador(configuracion['traduccion'], fixture)
        log.warning(datos)

        self.assertEqual(respuesta, datos)
        
