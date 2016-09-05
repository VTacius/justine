# coding: utf-8

import datetime
# Las siguientes librerías son parte del core actual, podrían volverse innecesarias cuando use la
# API de Samba4
from json import load, dump
from os import getcwd, remove, listdir

# No tendría sentido que manejemos logggin desde tan abajo de la aplicación, que no sea en desarrollo
import logging
log = logging.getLogger('justine')

class Usuarios:
   
    def __init__(self):
        self.direccion = getcwd()
    
    def listar(self):
        """
        Acá ocurrirá la más simple de todas las busquedas posibles: No más de 250 usuarios 
        """
        direccion = self.direccion + '/datos.d/'
        ficheros = listdir(direccion)
        usuarios = []
        for fichero in ficheros:
            if fichero.find('usuarios_detalle') == 0:
                fichero = open(direccion + '/' + fichero)
                contenido = load(fichero)
                # No importa el origen, es necesario asegurarse de limitar las claves que enviamos
                contenido_lite = { clave: contenido[clave] for clave in ['ou', 'givenName', 'sn', 'o', 'uid'] if clave in contenido }
                usuarios.append(contenido_lite)
        return usuarios

    def busqueda(self, filtros):
        if 'filtro' in filtros:
            termino = filtros['filtro'][0]
            direccion = self.direccion + '/datos.d/usuarios_busqueda.d/'
            ficheros = listdir(direccion)
            usuarios = []
            for fichero in ficheros:
                if fichero.find(termino) == 0:
                    fichero = open(direccion + '/' + fichero)
                    contenido = load(fichero)
                    # No importa el origen, es necesario asegurarse de limitar las claves que enviamos
                    # TODO: Agregar title sigue en discusión
                    # TODO: De agregarse title, lo más probable es que mail y telephoneNumber le sigan
                    contenido_lite = { clave: contenido[clave] for clave in ['ou', 'givenName', 'sn', 'title', 'o', 'uid'] if clave in contenido }
                    usuarios.append(contenido_lite)
        else:
            usuarios = self.listar()
        return usuarios

    def detalle(self, uid):
        """
        Acá obtenemos más detalles del usuario en base al rol del cliente
        TODO: Verificar rol del usuario
        """
        direccion = self.direccion + '/datos.d/usuarios_detalle_' + uid + '.json'

        # Verifica que el usuario existe
        try:
            fichero = open(direccion)
            contenido = load(fichero)
        except IOError as e:
            raise IOError
        except Exception as e:
            raise Exception(e.args)

        return contenido

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
            # Error de lectura, lo tomamos como que el fichero, por tanto el usuario, no existe 
            pass
        else:
            # Es posible abrir el archivo, el fichero, por tanto el usuario, no existe 
            raise IOError
        
        # Realizamos la operación Creación de Usuario 
        try:
            fichero = open(direccion, 'w')
            dump(contenido, fichero)
        except Exception as e:
            # TODO: Estoy pensando que todo esto deberia ir a logging, en lugar de cualquier otra parte
            raise Exception(contenido)
        
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
    
    def modificacion(self, uid, contenido):
        direccion = self.direccion + '/datos.d/usuarios_detalle_' + uid + '.json'

        # Verifica que el usuario existe
        try:
            fichero = open(direccion, 'r')
            contenido_original = load(fichero)
        except Exception as e:
            # Si no pudo abrir el archivo, es porque el usuario no existe
            raise IOError
       
        # ¿Qué claves le es posible cambiar?
        # Estas claves, por extraño que parezca, deberían estar disponibles o no
        # en función de la actividad que realiza y del rol que el usuario obstenta
        # De hecho, sólo puede usar esto dado un rol así que ni modo
        claves = ['sn', 'givenName', 'o', 'ou', 'dui', 'nit', 'fecha', 'title', 'pregunta', 'respuesta']
      
        for clave in claves:
            if clave in contenido:
                contenido_original[clave] = contenido[clave]
             
        # Realizamos operación de Modificacion de usuario
        try:
            fichero = open(direccion, 'w')
            dump(contenido_original, fichero)
        except Exception as e:
            raise Exception(e.args)

        return uid + " Parchado"

if __name__ == '__main__':
    u = Usuarios()
    #u.borrado('opineda')
    contenido = {'uid': 'ebonilla', 'givenName': 'Ericka'}
    u.actualizacion(contenido)
    
    pass
