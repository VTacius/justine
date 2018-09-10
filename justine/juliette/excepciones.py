#!/usr/bin/python2.7
# coding: utf-8

from exceptions import BaseException

class ConfiguracionException(BaseException):
    pass

class AutenticacionException(BaseException):
    pass

class OperacionException(BaseException):
    pass

class DatosException(BaseException):
    pass

class ConflictoException(BaseException):
    pass

class NoEntidadException(BaseException):
    pass
