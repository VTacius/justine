#!/usr/bin/python2.7
# coding: utf-8 

from cerberus import Validator
from ..juliette.excepciones import DatosException

class EsquemaUsuario():
    def __init__(self, *claves_requeridas):
        self.cadena = {'type': 'string'}
        self.boleano = {'type': 'boolean'}
        self.entero = {'type': 'integer'}
        self.correo = {'type': 'string', 'regex': "(?i)^[A-Z0-9._%!#$%&'*+-/=?^_`{|}~()]+@[A-Z0-9]+([.-][A-Z0-9]+)*\.[A-Z]{2,22}$"}
        self.telefono = {'type': 'string', 'regex': "^\d{4}(-*\d{4})*$"}
        # TODO: Esta puede mejorar, y tiene que estar en conformidad a lo que digamos en el cliente
        self.password = {'type': 'string', 'regex': "^(?=.*[A-Z])(?=.*\d)(?=.*[\.|_|#]).{8,}$"}
        self.cadena_enteros = {'type': 'string', 'regex': "[0-9]+"}
    
        esquema = {}
        esquema["givenName"] = self.cadena.copy()
        esquema["grupo"] = self.cadena_enteros.copy()
        esquema["grupos"] = {'type': 'list', 'schema': self.cadena_enteros.copy()}
        esquema["loginShell"] = self.cadena.copy()
        esquema["mail"] = self.correo.copy()
        esquema["o"] = self.cadena_enteros.copy()
        esquema["ou"] = self.cadena_enteros.copy()
        esquema["sambaAcctFlags"] = self.boleano.copy()
        esquema["sn"] = self.cadena.copy()
        esquema["telephoneNumber"] = self.telefono.copy()
        esquema["title"] = self.cadena.copy()
        esquema["uid"] = self.cadena.copy()
        esquema["userPassword"] = self.password.copy()
        
        esquema = self._requeridor(esquema, claves_requeridas) 

        self.validador = Validator(esquema)

    def _requeridor(self, esquema, claves_requeridas):
        for clave in claves_requeridas: 
            esquema[clave]['required'] = True

        return esquema
    
    def validacion(self, contenido):
        if self.validador.validate(contenido):
            return contenido
        else:
            raise DatosException(self.validador.errors)

