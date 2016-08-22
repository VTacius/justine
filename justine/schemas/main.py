# coding: utf-8

from iso8601.iso8601 import parse_date, ParseError
from cerberus import Validator

import re

class Validaciones(Validator):
    re_jvs = '^\d{1,12}$'
    jvs = re.compile(re_jvs)
    
    def _validate_type_fecha(self, campo, valor):
        try: 
            fecha = parse_date(valor).isoformat()
        except ParseError as e:
            self._error(campo, e.args)

    def _validate_type_jvs(self, campo, valor):
        try:
            estado = valor['estado']
            cadena = valor['valor']
            if estado:
                if not (isinstance(cadena, str) or isinstance(cadena, unicode)):
                    raise KeyError('Cadena debe ser del tipo string')
                if not self.jvs.match(cadena):
                    raise KeyError('La cadena no coindice con el requerimiento')
            else:
                return isinstance(cadena, bool)
                 
        except KeyError as e:
            self._error(campo, e.args) 
