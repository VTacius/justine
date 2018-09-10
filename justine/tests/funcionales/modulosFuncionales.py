# coding: utf-8

def creador_test():
    from justine import main
    from webtest import TestApp

    app = main({})
    testapp = TestApp(app)
    
    return testapp
    
def cargar_datos():
    from json import load
    fichero = open('/root/ambiente-justine/justine-api/justine/tests/datos.json', 'rb')
    contenido = load(fichero)

    return contenido

def credenciales(rol):
    # TODO: Podrías hacer esto aún menos público
    fixtures = {'credenciales': 
        {
            'administrador': {'usuario': 'alortiz', 'password': 'Figaro.12'},
            'tecnicosuperior': {'usuario': 'alortiz', 'password': 'alortiz'},
            'usuario': {'usuario': 'usuario', 'password': 'usuario'}
        }
    }

    from justine import main
    from webtest import TestApp

    app = main({})
    testapp = TestApp(app)

    try:
        credenciales = fixtures['credenciales'][rol]
    except Exception as e:
        pass
    
    auth = testapp.post_json('/auth/login', status=200, params=credenciales)
    return {'WWW-Authorization': str(auth.json_body['token'])}
