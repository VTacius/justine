# coding: utf-8

def creador_test():
    from justine import main
    from webtest import TestApp

    app = main({})
    testapp = TestApp(app)
    
    return testapp
    
def cargar_datos(entidad):
    from json import load
    fichero = open('/root/ambiente-justine/justine-api/justine/tests/datos.json', 'rb')
    contenido = load(fichero)

    return contenido[entidad]

def credenciales(rol):
    # Leer el README.md sobre como obtener un TOKEN
    # Pues si, por ahora no tenemos un sistema de roles como tal
    token = 'eyJyb2wiOiAiYWRtaW5pc3RyYWRvciIsICJkaXJlY2Npb24iOiAiYWxvcnRpeiJ9.3wR/qMGedccms7xFXN+GCbxlhbTknXGaBrtK3byOzJ0='
    return {'WWW-Authorization': token}
