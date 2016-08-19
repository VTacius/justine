# coding: utf-8

import datetime
# Las siguientes librerías son parte del core actual, podrían volverse innecesarias cuando use la
# API de Samba4
from json import load, dump
from os import getcwd, remove

class Usuarios:
   
    def __init__(self):
        self.direccion = getcwd()
    
    def esquema(self, contenido):
        """
        En realidad, suponemos que el trabajo de validación principal fue hecho de cara a la vista
        de nuestra API
        Sin embargo, convertimos fecha a algo serializable y desechamos todos aquellos datos que se nos envíen vacíos,
        tal expresa colander a los datos opcionales
        No espero complicar demasiado la validación respecto a datos opcionales y no, de eso se debe encargar el cliente
        """
        resultado = {}
        for clave in contenido:
            if isinstance(contenido[clave], datetime.date):
                resultado[clave] = contenido[clave].isoformat()
            elif contenido[clave]:
               resultado[clave] = contenido[clave] 
        
        return resultado

    def listar(self):
        """
        Acá ocurrirá la más simple de todas las busquedas posibles: No más de 250 usuarios 
        """
        direccion = self.direccion + '/datos.d/usuarios_listado.json'
        fichero = open(direccion)
        contenido = load(fichero)
        return contenido[:250]

    def detalle(self, uid):
        """
        Acá obtenemos más detalles del usuario en base al rol del cliente
        TODO: Verificar rol del usuario
        """
        direccion = self.direccion + '/datos.d/usuarios_detalle_' + uid + '.json'
        try:
            fichero = open(direccion)
            contenido = load(fichero)
        except IOError as e:
            raise Exception()
        return contenido

    def creacion(self, contenido):
        # TODO: Es necesario verificar el contenido recibido, o quizá confiar ciegamente en colander de la vista
        # Es importante verificar si el usuario ya existe
        uid = contenido['uid']
        direccion = self.direccion + '/datos.d/usuarios_detalle_' + uid + '.json'
        
        # Estamos verificando si el usuario existe
        try: 
            fichero = open(direccion)
        except IOError as e:
            # Si hubo un error de cualquier tipo respecto a abrir el fichero, no hacer nada, 
            # precisamente el fichero no debe existir
            pass
        else:
            # Si no ha habido error y el archivo se pudo abrir, significa de hecho que existe
            # y por tanto habrá que generar una excepción
            raise IOError
        
        # Realizamos la operación Creación de usuario 
        try:
            fichero = open(direccion, 'w')
            dump(contenido, fichero)
        except Exception as e:
            # TODO: Estoy pensando que todo esto deberia ir a logging, en lugar de cualquier otra parte
            #raise Exception()
            raise Exception( contenido)
        
        # Debería retornar, de hecho, la URL del nuevo objeto creado
        return "/usuarios/" + uid 

    def borrado(self, uid):
       
        direccion = self.direccion + '/datos.d/usuarios_detalle_' + uid + '.json'

        # Verifica si el usuario existe
        try: 
            fichero = open(direccion)
        except IOError as e:
            # Si no pudo abrir el archivo, es porque el usuario no existe
            # Devuelve error 404 al cliente
            raise ValueError
       
        # Realizamos la operación Borrado de usuario 
        try:
            contenido = remove(direccion)
        except Exception as e:
            # Este será un error más general, 
            # Devuelve error 500 al cliente
            raise Exception(e.args)
      
        return uid + " Borrado" 

    def actualizacion(self, uid, contenido):
        direccion = self.direccion + '/datos.d/usuarios_detalle_' + uid + '.json'

        # Verifica que el usuario existe
        try:
            fichero = open(direccion)
            contenido_original = load(fichero)
        except Exception as e:
            raise IOError

        # Comprobamos que el contenido recibido tenga el mismo contenido del objeto original
        claves = contenido_original.keys()
        for clave in claves:
            if clave not in contenido:
                contenido[clave] = contenido_original[clave]

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
            raise ValueError
       
        # Realizamos operación de parchado de usuario
        
        # ¿Qué claves le es posible cambiar?
        claves = ['sn', 'givenName', 'o', 'ou', 'dui', 'nit', 'fecha', 'title', 'pregunta', 'respuesta']
      
        for clave in claves:
            if clave in contenido:
                contenido_original[clave] = contenido[clave]
             
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
