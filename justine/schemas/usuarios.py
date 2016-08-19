# coding: utf-8 

from cerberus import Validator, ValidationError
from ..schemas.main import Validaciones

import logging
log = logging.getLogger('justine')

class Esquema():
    def __init__(self, *claves_requeridas):
        self.cadena = {'type': 'string'}
        self.boleano = {'type': 'boolean'}
        self.fecha = {'type': 'fecha'}
        self.entero = {'type': 'integer'}
        self.dui = {'type': 'string', 'regex': '^\d{9}-\d{1}$'}
        self.nit = {'type': 'string', 'regex': '^\d{4}-\d{6}-\d{3}-\d{1}$'}
        self.jvs = {'type': 'string', 'regex': '^\d{1,12}$'}
        self.correo = {'type': 'string', 'regex': "(?i)^[A-Z0-9._%!#$%&'*+-/=?^_`{|}~()]+@[A-Z0-9]+([.-][A-Z0-9]+)*\.[A-Z]{2,22}$"}
        self.telefono = {'type': 'string', 'regex': "^\d{4}(-*\d{4})*$/"}
        # TODO: Esta puede mejorar, y tiene que estar en conformidad a lo que digamos en el cliente
        self.password = {'type': 'string', 'regex': "^(?=.*[A-Z])(?=.*\d)(?=.*[\.|_|#]).{8,}$"}
    
        self.esquema = {}
        self.esquema["buzonStatus"] = self.boleano.copy()
        self.esquema["cuentaStatus"] = self.boleano.copy()
        self.esquema["dui"] = self.dui.copy()
        self.esquema["fecha"] = self.fecha.copy()
        self.esquema["givenName"] = self.cadena.copy()
        self.esquema["grupo"] = self.entero.copy()
        self.esquema["grupos"] = {'type': 'list', 'schema': self.entero.copy()}
        self.esquema["jvs"] = {"type": "dict", "schema": {"estado": self.boleano.copy(), "valor": self.cadena.copy()}}
        self.esquema["loginShell"] = self.cadena.copy()
        self.esquema["mail"] = self.correo.copy()
        self.esquema["nit"] = self.nit.copy()
        self.esquema["o"] = {"type": "dict", "schema": {"id": self.entero.copy(), "nombre": self.cadena.copy()}}
        self.esquema["ou"] = self.cadena.copy()
        self.esquema["pregunta"] = self.cadena.copy()
        self.esquema["respuesta"] = self.cadena.copy()
        self.esquema["sambaAcctFlags"] = self.boleano.copy()
        self.esquema["sn"] = self.cadena.copy()
        self.esquema["telephoneNumber"] = self.telefono.copy()
        self.esquema["title"] = self.cadena.copy()
        self.esquema["uid"] = self.cadena.copy()
        self.esquema["userPassword"] = self.password.copy()
        self.esquema["usoBuzon"] = self.entero.copy()
        self.esquema["volumenBuzon"] = self.entero.copy()
        log.error(claves_requeridas)        
        self.esquema = self._requeridor(self.esquema, claves_requeridas) 

    def _requeridor(self, esquema, claves_requeridas):
        for clave in claves_requeridas: 
            esquema[clave]['required'] = True

        return esquema

class EsquemaCreacion(Esquema):
    """
    Requeridos: uid
    Para todos los demás, opcionales, es preciso verificarlos de encontrarse presentes
    """
    def __init__(self, *claves_requeridas):
        Esquema.__init__(self, *claves_requeridas)
        self.validador = Validaciones(self.esquema)
    
    def validacion(self, contenido):
        if self.validador.validate(contenido):
            return contenido
        else:
            raise ValidationError(self.validador.errors)

class EsquemaActualizacion(Esquema):
    """
    Va resultando que incluso acá son todas opcionales
    """
    def __init__(self, *claves_requeridas):
        Esquema.__init__(self, *claves_requeridas)
        self.validador = Validaciones(self.esquema)

    def validacion(self, contenido):
        if self.validador.validate(contenido):
            return contenido
        else:
            raise ValidationError(self.validador.errors)
 
class EsquemaModificacion(Esquema):
    def __init__(self):
        Esquema.__init__(self, *claves_requeridas)

# Necesito usar un patrón (No recuerdo el nombre pero si que hace) 
# porque el objeto usuario a crear depende de la vista que nos envíe el json
# e incluso del nivel de usuario, creo que este último puede encapsularse en diferentes vistas
class EsquemaUsuario():
    
    @staticmethod
    def obtener(tipo, *claves_requeridas):
        if tipo == "creacion":
            return EsquemaCreacion(*claves_requeridas)
        elif tipo == "actualizacion":
            return EsquemaActualizacion(*claves_requeridas) 
        elif tipo == "modificacion":
            return EsquemaModificacion(*claves_requeridas)
        else:
            raise TypeError

