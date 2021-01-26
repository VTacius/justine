#!/usr/bin/python2.7 
# coding: utf-8

from .modelBase import Base, operacion, diccionador, ldifeador, normalizador
from .excepciones import ConflictoException, OperacionException, DatosException

from ldb import SCOPE_SUBTREE, OID_COMPARATOR_AND
from samba.dsdb import UF_NORMAL_ACCOUNT

import logging
log = logging.getLogger('justine')

# La idea es que esto defina gran parte del comportamiento de la clase
configuracion = {
        'claves': ['cn', 'type', 'description', 'mail', 'notes'],
        'traduccion' : {'cn': 'groupName', 'mail': 'mailaddress'},
        'borrables': ['objectSid', 'objectGUID']
}

# Este es el GID mínimo para grupo. Int por favor
GRUPO_MINIMO_GID = 1005 

class Grupo(Base):
    
    def __init__(self):
        super(Grupo, self).__init__(configuracion)
        
        # Desde Base, tenemos: lp, creds, conexion, claves, borrables, traduccion

    @operacion
    def crear(self, grupo, datos):
        existe = len(self.__buscar_grupo(self.conexion, grupo)) > 0
        if existe:
            log.warning("El grupo %s ya existe" % grupo)
            raise ConflictoException("El grupo %s ya existe" % grupo)
        
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
    
    @operacion
    def borrar(self, grupo):
        contenido = self.__buscar_grupo(self.conexion, grupo)
        if len(contenido) == 0:
            raise ConflictoException('El grupo %s no existe' % grupo) 
        
        self.conexion.deletegroup(grupo)
 
        return "Eliminado el grupo %s" % grupo
