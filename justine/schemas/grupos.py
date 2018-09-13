#!/usr/bin/python2.7
# coding: utf-8 

from cerberus import Validator
from ..juliette.excepciones import DatosException

class EsquemaGrupo():
    def __init__(self, *claves_requeridas):
        self.cadena = {'type': 'string'}
        self.correo = {'type': 'string', 'regex': "(?i)^[A-Z0-9._%!#$%&'*+-/=?^_`{|}~()]+@[A-Z0-9]+([.-][A-Z0-9]+)*\.[A-Z]{2,22}$"}
        self.cadena_enteros = {'type': 'string', 'regex': "[0-9]+"}
    
        esquema = {}
        esquema["cn"] = self.cadena.copy()
        esquema["type"] = self.cadena_enteros.copy()
        esquema["description"] = self.cadena.copy()
        esquema["mail"] = self.correo.copy()
        esquema["notes"] = self.cadena.copy()
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

