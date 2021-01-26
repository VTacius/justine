#!/usr/bin/python2.7
# coding: utf-8

from samba import Ldb
from samba.credentials import Credentials
from samba.param import LoadParm
from samba.auth import user_session, system_session, AUTH_SESSION_INFO_DEFAULT_GROUPS, AUTH_SESSION_INFO_AUTHENTICATED, AUTH_SESSION_INFO_SIMPLE_PRIVILEGES

from ldb import SCOPE_SUBTREE, LdbError

session_info_flags = ( AUTH_SESSION_INFO_DEFAULT_GROUPS | AUTH_SESSION_INFO_AUTHENTICATED )

import logging
log = logging.getLogger('justine')

from .excepciones import ConfiguracionException 

def parametros(fichero=False):
    """
    Intento ser un poco cuidadoso con la forma en que obtenemos la configuración
    """
    try:
        lp = LoadParm()
        lp.load_default() if fichero is False else lp.load(fichero)
        return lp
    except RuntimeError as e:
        log.warning(e.message)
        raise ConfiguracionException(e)


def credenciales(username, password, parametros):
    """
    Más que nada, encapsulo un par de líneas sobre el trabajo con Credentials()
    Rompe un poco la idea de inyección, pero así las cosas
    """
    cred = Credentials()
    dominio = parametros.get('workgroup')
    
    cred.set_username(username)
    cred.set_password(password)
    cred.set_domain(dominio)
    
    # TODO: ¿Este tiene algún efecto?
    cred.set_workstation("")

    return cred

def conectar(lp):
    """
    Cumple con la idea de inyección, así que debería ser testeable
    """
    try:
        sesion = system_session()

    except LdbError as e:
        log.warning("Error LDB: %s" % e)
        return False;
    except Exception as e:
        log.warning("Error no contemplado %s " % e)
        return False;
    
    return sesion

def autenticacion(creds, lp):
    """
    Cumple con la idea de inyección, así que debería ser testeable
    """
    try:
        ldap_conn = Ldb('ldap://localhost', lp=lp, credentials=creds)
        
        domain_dn = ldap_conn.get_default_basedn()
        search_filter='sAMAccountName={0}'.format(creds.get_username())
       
        # NOTA: No intentes usar searchone para este caso específico. Dn resulta ser una clase no iterable
        busqueda = ldap_conn.search(base=domain_dn, scope=SCOPE_SUBTREE, expression=search_filter, attrs=['dn', 'memberOf', 'displayName'])
        user_dn = busqueda[0].dn
       
        sesion = user_session(ldap_conn, lp_ctx=lp, dn=user_dn, session_info_flags=session_info_flags)

        # Este punto podría ser importante para la idea de login
        token = sesion.security_token

    except LdbError as e:
        log.warning("Error LDB: %s" % e)
        return False;
    except IndexError as e:
        log.warning("El usuario %s no existe" % creds.get_username())
        return False;
    except Exception as e:
        log.warning("Error no contemplado %s " % e)
        return False;
   
    return busqueda

