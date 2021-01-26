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
        'claves': ['givenName', 'grupo', 'grupos', 'loginShell', 'mail', 'o', 'ou', 'sambaAcctFlags', 'sn', 'telephoneNumber', 'title', 'uid', 'userPassword'],
        'traduccion' : {'title': 'jobtitle', 'sn': 'surname', 'userPassword': 'password', 'o': 'company', 'ou': 'department', 'mail': 'mailaddress', 'grupo': 'gidnumber'},
        'borrables': ['objectSid', 'objectGUID']
}

# Este es el UID mínimo para usuario. Int por favor
USUARIO_MINIMO_UID = 1005 

# Este es el grupo por defecto. Sí, debe ser Str
GRUPO_POR_DEFECTO = "1005"

class Usuario(Base):
    """
    TODO: Registrar la mayor cantidad posible de información 
    """

    def __init__(self):
        super(Usuario, self).__init__(configuracion)
       
        # Desde Base, tenemos: lp, creds, conexion, claves, borrables, traduccion
  
    def __buscar_grupos(self, conexion, g):
        filtro = '(&(objectClass=group)(|(gidNumber={0})(cn={0})))'.format
        
        domain_dn = conexion.get_default_basedn()
        busqueda = conexion.search(base=domain_dn, scope=SCOPE_SUBTREE, expression=filtro(g), attrs=['cn'])
        
        if len(busqueda) > 0:
            elemento = busqueda[0]
            grupo = elemento.get('cn')[0]
            return grupo
        else: 
            msg = 'No encontré tal grupo: {0}'.format(g)
            log.warning(msg)

    def __grupear(self, conexion, grupos):
        """
        Auxiliar para self.__configurar_grupos
        """
        resultado = []
        for g in grupos:
            grupo = self.__buscar_grupos(conexion, g)
            if grupo:
                resultado.append(grupo)

        return resultado

    def __configurar_grupos(self, conexion, usuario, grupos, grupos_actuales = []):
        """
        Agrego/remuevo grupos
        """
        grupos_nuevos = self.__grupear(conexion, grupos) 
        
        grupos_actuales = [x.split(',')[0].split('=')[1] for x in grupos_actuales]
        grupos_ya_configurados = self.__grupear(conexion, grupos_actuales)
       
        for grupo in grupos_nuevos:
            if grupo not in grupos_ya_configurados:
                conexion.add_remove_group_members(grupo, [usuario], add_members_operation=True)
       
        for grupo in grupos_ya_configurados:
            if grupo not in grupos_nuevos:
                conexion.add_remove_group_members(grupo, [usuario], add_members_operation=False)
        
    def __verificar_gidNumber(self, conexion, datos):
        """
        Es imperativo revisar que el gidNumber dado exista
        """
        gidNumber = datos.get('grupo', GRUPO_POR_DEFECTO)
        
        domain_dn = conexion.get_default_basedn()
        filtro = '(&(objectClass=group)(gidNumber={0}))'.format(gidNumber)
        busqueda = conexion.search(base=domain_dn, scope=SCOPE_SUBTREE, expression=filtro, attrs=['cn'])
        if len(busqueda) == 0:
            msg = 'gidNumber proporcionado {0} no se corresponde con un grupo existente'.format(gidNumber)
            log.warning(msg)
            raise DatosException(msg)
        else:
            return gidNumber

    def __configurar_estado(self, conexion, usuario, isActivo):
        """
        Usamos la librería subyacente para configurar el estado del usuario
        """
        filtro_usuario = 'sAMAccountName={0}'.format(usuario.decode())
        if isActivo:
            conexion.enable_account(filtro_usuario)
        else:
            conexion.disable_account(filtro_usuario)
        

    @operacion
    def crear(self, usuario, datos):    
        existe = len(self.__buscar_usuario(self.conexion, usuario)) > 0
        if existe:
            log.warning("El usuario %s ya existe" % usuario)
            raise ConflictoException("El usuario %s ya existe" % usuario)
        
        # ¿El usuario esta activo dentro del dominio? Por defecto, lo estará
        esActivo = datos.pop('sambaAcctFlags', True)
    
        # Lista de grupos para el usuario
        grupos = datos.pop('grupos')

        # Pues no, por el momento dejaremos lo de cambiar el uid
        datos.pop('uid', '')

        # Verificamos que el grupo configurado exista, y damos como grupo por defecto al primero
        datos['gidNumber'] = self.__verificar_gidNumber(self.conexion, datos)
       
        datos['uidNumber'] = self._obtener_uid_number(USUARIO_MINIMO_UID, 'uidNumber')
        
        datos['nisDomain'] = self.get_nisdomain()

        # Efectuamos la creación propiamente dicha
        datos = normalizador(self.traduccion, datos)
        self.conexion.newuser(usuario, **datos)
        
        # Operaciones secundarias: Estado de la cuenta dentro del dominio
        self.__configurar_estado(self.conexion, usuario, esActivo) 

        # Operaciones secundarias: Configuramos los grupos
        self.__configurar_grupos(self.conexion, usuario.decode(), grupos)
       
        # Operaciones secundarias: Es que necesito esto, de lo contrario, no es posible configurar contraseña
        password = datos.get('password')
        self.conexion.setpassword("(samAccountName=%s)" % usuario.decode(), password)

        return "Creado el usuario %s" % usuario.decode()
   
    def __buscar_usuario(self, conexion, usuario=False, attrs=False):
        claves = attrs.split(',') if type(attrs) == str else attrs
        if usuario:
            expresion = 'sAMAccountName={0}'.format(usuario)
        else:
            expresion = '(&(objectClass=user)(userAccountControl:{0}:={1}))'.format(OID_COMPARATOR_AND, UF_NORMAL_ACCOUNT) 
        return self._buscar_entidad(conexion, expresion, claves)

    @operacion   
    def obtener(self, usuario=False, attrs=False):
        resultado = self.__buscar_usuario(self.conexion, usuario, attrs)

        if len(resultado) == 0:
            raise DatosException('No se encontraron datos') 
        
        return resultado

    def __dateador_usuario(self, traduccion_claves, datos_actuales, datos_nuevos):
       
        # Obtenemos los datos referidos al nombre
        givenName = datos_actuales.get('givenName', '') if 'givenName' not in datos_nuevos else datos_nuevos.pop('givenName')
        surname = datos_actuales.get('sn', '') if 'sn' not in datos_nuevos else datos_nuevos.pop('sn')
        
        # Creamos el nombre
        displayName = givenName + " " + surname
    
        # Obviamos de la traducción aquellos atributos que no necesitan traducción
        traduccion_claves.pop('title', '')
        traduccion_claves.pop('mail', '')
        # TODO: Con sn es extraño, a veces parece que este no existe
        traduccion_claves.pop('sn', '')
       
        # TODO: Existe un atributo 'name', que sin embargo necesita una operacion 'rename', que si embargo no funciona tal como se espera
        resultado = {
            "sn": surname,
            "givenName": givenName,
            "displayName": displayName
        }
    
        resultado = normalizador(traduccion_claves, datos_nuevos, resultado)

        return resultado

    def __revisar_claves_existentes(self, datos_actuales, datos_nuevos):
        for clave in self.claves:
            if clave in datos_actuales and clave not in datos_nuevos:
                raise DatosException('No puede eliminar datos del usuario')
    
    @operacion
    def actualizar(self, usuario, datos_nuevos, completo=True):
        contenido = self.__buscar_usuario(self.conexion, usuario)
        if len(contenido) == 0:
            raise ConflictoException('El usuario %s no existe' % usuario) 

        datos_actuales = contenido[0]

        if completo:
            self.__revisar_claves_existentes(datos_actuales, datos_nuevos)

        # Verificamos que el grupo exista. 
        # Por consistencia, no haremos nada más hasta que estemos seguros
        if 'grupo' in datos_nuevos:
            grupo = self.__verificar_gidNumber(self.conexion, datos_nuevos)

        # Operaciones secundarias: Estado de la cuenta dentro del dominio
        if 'sambaAcctFlags' in datos_nuevos:
            isActivo = datos_nuevos.pop('sambaAcctFlags')
            self.__configurar_estado(self.conexion, usuario, isActivo) 
        
        # Operaciones secundarias: Configuramos los grupos
        if 'grupos' in datos_nuevos:
            grupos = datos_nuevos.pop('grupos')
            if 'memberOf' in datos_actuales:
                memberOf = datos_actuales['memberOf']
                grupos_actuales = memberOf if type(memberOf) == list else [memberOf]
                self.__configurar_grupos(self.conexion, usuario, grupos, grupos_actuales)
            else:
                self.__configurar_grupos(self.conexion, usuario, grupos)

        # Operaciones secundadarias: Configuramos contraseña
        if 'userPassword' in datos_nuevos:
            password = datos_nuevos.pop('userPassword')
            self.conexion.setpassword('sAMAccountName={0}'.format(usuario), password)
            # Pues sí, debido a nuestro problema donde al parecer es posible usar la contraseña anterior
            self.conexion.setpassword('sAMAccountName={0}'.format(usuario), password)

        # Operación principal
        if datos_nuevos:
            traductores = self.traduccion.copy()

            datos_nuevos = self.__dateador_usuario(traductores, datos_actuales, datos_nuevos)
            ldif = ldifeador(datos_actuales, datos_nuevos)
            self.conexion.modify_ldif(ldif)
    
        return "Actualizado el usuario %s" % usuario

    @operacion
    def borrar(self, usuario):
        contenido = self.__buscar_usuario(self.conexion, usuario)
        if len(contenido) == 0:
            raise ConflictoException('El usuario %s no existe' % usuario) 
        
        self.conexion.deleteuser(usuario)
 
        return "Eliminado el usuario %s" % usuario
