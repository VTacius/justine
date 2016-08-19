# coding: utf-8

from iso8601.iso8601 import parse_date, ParseError
from cerberus import Validator


class Validaciones(Validator):
    
    def _validate_type_fecha(self, campo, valor):
        try: 
            fecha = parse_date(valor).isoformat()
        except ParseError as e:
            self._error(campo, e.args)
