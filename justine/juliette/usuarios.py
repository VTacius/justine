# coding: utf-8

from json import load, dump

# Las siguientes librerías son parte del core actual, podrían volverse innecesarias cuando use la
# API de Samba4
from os import getcwd, remove

class Usuarios:
   
    def __init__(self):
        self.direccion = getcwd()

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
            raise Exception(e.args)
        
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
        except Exception as e:
            raise ValueError

        # Realizamos la operacion Actualización de Usuario
        try:
            fichero = open(direccion, 'w')
            dump(contenido, fichero)
        except Exception as e:
            # Este será un error más general, 
            # Devuelve error 500 al cliente
            print e.args
            raise Exception(e.args)

        return uid + " Actualizado"
            

if __name__ == '__main__':
    u = Usuarios()
    #u.borrado('opineda')
    contenido = {'uid': 'ebonilla', 'givenName': 'Ericka'}
    u.actualizacion(contenido)
    
    pass
