# coding: utf-8

# Excepciones con nombres llamativos ayudarán a la legibilidad del código
from ..juliette.Exceptions import RolInvalido, PermisosInsuficientes

import datetime
# Las siguientes librerías son parte del core actual, podrían volverse innecesarias cuando use la
# API de Samba4
from json import load, dump
from os import getcwd, remove, listdir

# No tendría sentido que manejemos logggin desde tan abajo de la aplicación, que no sea en desarrollo
import logging
log = logging.getLogger('justine')

class Usuarios:
    @staticmethod
    def createAs(username, rol):
        claves_ligeras = ['givenName', 'mail', 'o', 'ou', 'sn', 'telephoneNumber', 'title', 'uid']
        # Estas son las claves. A pesar de las limitaciones con los demás usuarios, cada usuario puede manipular la mayoría 
        # de sus propios cambios a su antojo
        claves = ['buzonStatus', 'cuentaStatus', 'dui', 'fecha', 'givenName', 'grupo', 'grupos', 'loginShell', 'mail', 'nit', 'o', 
                'ou','pregunta', 'respuesta', 'sambaAcctFlags', 'sn', 'telephoneNumber', 'title', 'uid', 'userPassword', 
                'usoBuzon', 'volumenBuzon']
        if rol == 'usuario':
            claves_detalle = ['givenName', 'grupo', 'grupos', 'mail', 'o', 'ou', 'sn', 'telephoneNumber', 'title', 'uid']
            claves_modificacion = ['sn', 'givenName', 'o', 'ou', 'dui', 'nit', 'fecha', 'title', 'pregunta', 'respuesta']
            return Usuario(username, claves, claves_ligeras, claves_detalle, claves_modificacion)
        elif rol == 'tecnicosuperior':
            claves_detalle = ['buzonStatus', 'cuentaStatus', 'givenName', 'grupo', 'grupos', 'loginShell', 'mail', 'o', 
                'ou', 'sambaAcctFlags', 'sn', 'telephoneNumber', 'title', 'uid', 'userPassword', 'usoBuzon', 'volumenBuzon']
            claves_modificacion = ['sn', 'givenName', 'o', 'ou', 'dui', 'nit', 'fecha', 'title', 'pregunta', 'respuesta']
            return UsuarioTecnico(username, claves, claves_ligeras, claves_detalle, claves_modificacion)
        elif rol == 'administrador':
            claves_detalle = ['buzonStatus', 'cuentaStatus', 'dui', 'fecha', 'givenName', 'grupo', 'grupos', 'loginShell', 'mail', 'nit', 'o', 
                'ou','pregunta', 'respuesta', 'sambaAcctFlags', 'sn', 'telephoneNumber', 'title', 'uid', 'userPassword', 
                'usoBuzon', 'volumenBuzon']
            claves_modificacion = ['sn', 'givenName', 'o', 'ou', 'dui', 'nit', 'fecha', 'title', 'pregunta', 'respuesta']
            return UsuarioAdministrador(username, claves, claves_ligeras, claves_detalle, claves_modificacion)
        else:
            # No tenemos un rol válido, lanzamos un error personalizado RolInvalido
            raise RolInvalido("{} con {}".format(username, rol)) 

class Usuario:
   
    def __init__(self, username, claves, claves_ligeras, claves_detalle, claves_modificacion):
        self.direccion = getcwd()
        self.username = username
        self.claves = claves
        self.claves_ligeras = claves_ligeras 
        self.claves_detalle = claves_detalle 
        self.claves_modificacion = claves_modificacion 
        
    def __obtener_contenido(self, fichero, claves):
        """
        No espero que este método sobreviva cuando use la API de Samba
        """
        fichero = open(fichero)
        datos = load(fichero)
        # No importa el origen, es necesario asegurarse de limitar las claves que enviamos
        contenido = { clave: datos[clave] for clave in claves if clave in datos }
        return contenido

    def listar(self):
        """
        Acá ocurrirá la más simple de todas las busquedas posibles: No más de 250 usuarios 
        """
        direccion = self.direccion + '/datos.d/'
        ficheros = listdir(direccion)
        usuarios = []
        for fichero in ficheros:
            if fichero.find('usuarios_detalle') == 0:
                ruta = direccion + '/' + fichero
                usuarios.append(self.__obtener_contenido(ruta, self.claves_ligeras))
        return usuarios

    def busqueda(self, filtros):
        """
        Por ahora, es obvio que esto es una calco de Usuarios.listar(), estoy esperando que en algún
        momento se complique en serio así que lo separo desde ya
        """
        if 'filtro' in filtros:
            termino = filtros['filtro'][0]
            direccion = self.direccion + '/datos.d/usuarios_busqueda.d/'
            ficheros = listdir(direccion)
            usuarios = []
            for fichero in ficheros:
                if fichero.find(termino) == 0:
                    ruta = direccion + '/' + fichero
                    usuarios.append(self.__obtener_contenido(ruta, self.claves_ligeras))
        else:
            usuarios = self.listar()
        return usuarios
 
    def detalle(self, uid):
        """
        Acá obtenemos más detalles del usuario en base al rol del cliente
        """
        direccion = self.direccion + '/datos.d/usuarios_detalle_' + uid + '.json'
        # El rol determina con claves_detalle los atributos que puede obtener de cada usuario
        # Excepto si intenta obtener sus propios datos 
        claves = self.claves if self.username == uid else self.claves_detalle
            
        try:
            contenido = self.__obtener_contenido(direccion, claves)
        except IOError as e:
            # Verifica que el usuario existe
            raise IOError
        except Exception as e:
            # Cualquier otro error arroja un genérico 500 en la vista    
            raise Exception(e.args)
 
        return contenido
 
    def _modificacion(self, uid, contenido):
        """
        La idea es modificar una lista arbritraria de atributos 
        siempre que tenga permiso de hacerlo 
        """
        direccion = self.direccion + '/datos.d/usuarios_detalle_' + uid + '.json'

        # Verifica que el usuario existe
        try:
            fichero = open(direccion, 'r')
            contenido_original = load(fichero)
        except Exception as e:
            # Si no pudo abrir el archivo, es porque el usuario no existe
            raise IOError
      
        for clave in self.claves_modificacion:
            if clave in contenido:
                contenido_original[clave] = contenido[clave]
             
        # Realizamos operación de Modificacion de usuario
        try:
            fichero = open(direccion, 'w')
            dump(contenido_original, fichero)
        except Exception as e:
            raise Exception(e.args)

        return uid + " Parchado"
    
    def modificacion(self, uid, contenido):
        """
        Esta clase se limita a modificar un objeto con self.__modificacion
        si es que el usuario tiene permiso específico sobre dicho objeto, 
        en este caso, es el mismo objeto que representa al usuario
        """
        if uid == self.username:
            return self._modificacion(uid, contenido)
        else:
            raise PermisosInsuficientes(self.username + ' modificando a ' + uid) 

class UsuarioTecnico(Usuario):
   
    def __init__(self, username, claves, claves_ligeras, claves_detalle, claves_modificacion):
        Usuario.__init__(self, username, claves, claves_ligeras, claves_detalle, claves_modificacion)
    
    def modificacion(self, uid, contenido):
        # TODO: Existe un rol en el que esta modificación ocurre sólo con unos cuantos usuarios
        return Usuario._modificacion(uid, contenido)

class UsuarioAdministrador(Usuario):
   
    def __init__(self, username, claves, claves_ligeras, claves_detalle, claves_modificacion):
        Usuario.__init__(self, username, claves, claves_ligeras, claves_detalle, claves_modificacion)
        
    def modificacion(self, uid, contenido):
        # Podemos modificar cuantos usuarios querramos mediante self.__modificacion 
        return Usuario._modificacion(self, uid, contenido)
    
    def borrado(self, uid):
       
        direccion = self.direccion + '/datos.d/usuarios_detalle_' + uid + '.json'

        # Verifica si el usuario existe
        try: 
            fichero = open(direccion)
        except IOError as e:
            # Si no pudo abrir el archivo, es porque el usuario no existe
            raise IOError
       
        # Realizamos la operación Borrado de usuario 
        try:
            contenido = remove(direccion)
        except Exception as e:
            # Este será un error más general, 
            # Devuelve error 500 al cliente
            raise Exception(e.args)
      
        return uid + " Borrado" 

    def creacion(self, contenido):
        # TODO: Es necesario verificar el contenido recibido, o quizá confiar ciegamente en colander de la vista
        uid = contenido['uid']
        direccion = self.direccion + '/datos.d/usuarios_detalle_' + uid + '.json'
        
        # Verifica que el usuario existe
        try: 
            fichero = open(direccion)
        except IOError as e:
            # Error de lectura: El fichero, por tanto el usuario, no existe 
            pass
        else:
            # Es posible abrir el archivo: El fichero, por tanto el usuario, existe 
            raise IOError
        
        # Realizamos la operación Creación de Usuario 
        try:
            fichero = open(direccion, 'w')
            dump(contenido, fichero)
        except Exception as e:
            # TODO: Estoy pensando que todo esto deberia ir a logging, en lugar de cualquier otra parte
            raise Exception(e)
        
        # Debería retornar, de hecho, la URL del nuevo objeto creado
        return "/usuarios/" + uid 

    def actualizacion(self, uid, contenido):
        direccion = self.direccion + '/datos.d/usuarios_detalle_' + uid + '.json'

        # Verifica que el usuario existe
        try:
            fichero = open(direccion)
            contenido_original = load(fichero)
        except Exception as e:
            raise IOError

        # Comprobamos que el contenido recibido tenga todos los atributos que el contenido original ya tenía
        claves_contenido_original =  contenido_original.keys()
        claves_contenido_nuevo = contenido.keys()
        for clave in claves_contenido_original:
            if not clave in claves_contenido_nuevo:
                raise KeyError('Faltan claves para actualizar' + clave)

        # Realizamos la operacion Actualización de Usuario
        try:
            fichero = open(direccion, 'w')
            dump(contenido, fichero)
        except Exception as e:
            # Este será un error más general, 
            # Devuelve error 500 al cliente
            raise Exception(e.args)

        return uid + " Actualizado"
