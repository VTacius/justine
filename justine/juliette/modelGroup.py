#!/usr/bin/python2.7 # coding: utf-8

from modelBase import Base, operacion, diccionador, ldifeador, normalizador
from excepciones import OperacionException, DatosException

from ldb import SCOPE_SUBTREE, OID_COMPARATOR_AND
from samba.dsdb import UF_NORMAL_ACCOUNT

import logging
log = logging.getLogger('justine')

# La idea es que esto defina gran parte del comportamiento de la clase
configuracion = {
        'claves': [],
        'traduccion' : {},
        'borrables': ['objectSid', 'objectGUID']
}

# Este es el GID mínimo para usuario. Int por favor
GRUPO_MINIMO_GID = 1005 

class Grupo(Base):
    
    def __init__(self):
        super(Grupo, self).__init__()
        
        self.claves = configuracion['claves']
        self.traduccion = configuracion['traduccion']
        self.borrables = configuracion['borrables']
        
        # Desde Base, tenemos: lp, creds, conexion 

    @operacion
    def crear(self, grupo, datos):
        datos['nisDomain'] = self.get_nisdomain()

        datos['gidNumber'] = self._obtener_uid_number(GRUPO_MINIMO_GID, 'gidNumber')

        datos = normalizador(self.traduccion, datos)
        self.conexion.newgroup(**datos)

    def __buscar_grupo(self, conexion, grupo=False, attrs=False):
        if grupo:
            expresion = 'sAMAccountName={0}'.format(grupo)
        else:
            expresion = '(&(objectClass=group))'
    
        return self._buscar_entidad(self.conexion, expresion, attrs)

    @operacion
    def obtener(self, grupo=False, attrs=False):
        resultado = self.__buscar_grupo(self.conexion, grupo, attrs)

        if len(resultado) == 0:
            raise DatosException('No se encontraron datos') 
        return resultado
