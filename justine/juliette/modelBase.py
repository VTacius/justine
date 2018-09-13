#!/usr/bin/python2.7
# coding: utf-8

from excepciones import AutenticacionException, DatosException
from conexion import parametros, credenciales, conectar

from ldb import SCOPE_SUBTREE
from samba.samdb import SamDB

import logging
log = logging.getLogger('justine')

from excepciones import ConfiguracionException, OperacionException

class Base(object):
    def __init__(self):
        """
        Se encarga de retornar un objeto SamDB, lista a usar en la operación que querramos
        """
        self.lp = parametros()
        
        self.sesion = conectar(self.lp)
        if (self.sesion):
            self.conexion = SamDB(session_info=self.sesion, lp=self.lp)
        else:
            raise AutenticacionException('No estás autenticado')

    def get_nisdomain(self):
        return self.lp.get('workgroup')
    
    def __buscar_uid_disponible(self, uid_minimo, listado_actual):
	listado_actual.sort()
	
	inicio = uid_minimo
	final = listado_actual[-1]
	
	if final < inicio:
	    # Acá, posiblemente un return
	    return  inicio
	else:
	    lista_a_buscar = range(inicio, final)
	    for i in lista_a_buscar:
	        if i not in listado_actual:
	            return i
	   
	    return listado_actual[-1] + 1

    def _obtener_uid_number(self, minimo, uid):
        contenido = self.obtener(attrs=[uid])
        listado = [int(item[uid]) for item in contenido if uid in item]
        
	return str(self.__buscar_uid_disponible(minimo, listado))

    def _buscar_entidad(self, conexion, expresion, attrs=False):
        domain_dn = conexion.domain_dn()
        
        if attrs:
            resultado = conexion.search(domain_dn, scope=SCOPE_SUBTREE, expression=(expresion), attrs=attrs)
        else:
            resultado = conexion.search(domain_dn, scope=SCOPE_SUBTREE, expression=(expresion))
        
        contenido = [diccionador(self.borrables, u) for u in resultado]
        return contenido

def __definidor(indice, contenido):
    """
    TODO: Es necesario cambiar la razón por la cual se devuelve o no un listado:
     La condición debería ser "indice in lista"
     siendo "lista" precisamente los atributos que deben ser multivalor
    """
    resultado = contenido.get(indice)
    resultado = [u for u in contenido.get(indice)]
    if len(resultado) > 1:
        return resultado
    else:
        return resultado[0]

def diccionador(borrables, item):
    """
    Obtengo una lista o una valor cadena.
    NOTA: La mejora de las condiciones para que tipo de valor devuelve deben revisarse en __definidor
    TODO: ¿Quedaría mejor si diccionador fuera un método de Base, siendo borrables un atributo?
    """
    resultado = {}
    for i in item.keys():
        if i == "dn":
            resultado['dn'] = item.dn.extended_str()
        elif i not in borrables:
            resultado[i] = __definidor(i, item)
    return resultado

def ldifeador(datos_actuales, datos_nuevos):
    """
    LDIF, tu momento de brilla ha llegado
    TODO: Aunque no se haya considerado en la aplicación original, en algún momento debería 
     considerarse atributos con dos o más valores
    TODO: Por otra parte, podría convenir el usar un parseador algo más "profesional" Resulta que internamente, modify_ldif usa un parser que no envía errores más que a pantalla, triste
    """
    
    contenido = 'dn: {0}\n'.format(datos_actuales['dn'])
    contenido += 'changetype: modify\n'
    for d in datos_nuevos.keys():
        contenido += '-\nreplace: {0}\n'.format(d)
        contenido += '{0}: {1}\n'.format(d, datos_nuevos[d].encode('utf-8'))
    
    return contenido

def normalizador(traduccion_claves, datos, result = False):
    """
    Para cada atributo en dato, convierte la clave a minúscula y se asegura que esta sea ascii; 
     luego, encodea cada dato como utf-8, algo sumamente necesario para meterlo a samDB sin problema
    Además, cumple con una decisión de diseño: Mantener los nombres de claves del esquema original, 
     razón por la cual es necesario traducir
    """

    # Este es algo que tendrás que recordar por el resto de tu vida
    resultado = {} if not result else result
    for k in datos.keys():
        clave = k.lower() if k not in traduccion_claves else traduccion_claves[k].lower()
        c = clave.encode('ascii', 'ignore')
        d = datos[k].encode('utf-8')
        resultado[c] = d
    return resultado
    
def operacion(func):
    def wrapper(*datos, **argumentos):
        try:
            return func(*datos, **argumentos)
        except ConfiguracionException as e:
            log.warning(e)
            raise ConfiguracionException(e)
        except AutenticacionException as e:
            log.warning(e)
            raise AutenticacionException(e)
        except TypeError as e:
            # Intento de pasar argumentos desconocidos para las funciones propias de la API Samba
            log.warning(e)
            raise DatosException(e)
        except Exception as e:
            log.warning(e)
            if isinstance(e.args, tuple):
                if e.args[0] in [16, 67, 68]:
                    raise OperacionException(e.args[1])
                else:
                    msg = e.args[0]
                    if msg.find('Unable to find user') == 0 or msg.find('unable to parse ldif string') == 0 or msg.find('unable to import dn object') == 0:
                        raise OperacionException(e)
            raise Exception(e)


    return wrapper

