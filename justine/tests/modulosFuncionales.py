# coding: utf-8

def credenciales(rol):
    # TODO: Podrías hacer esto aún menos público
    fixtures = {'credenciales': 
        {
            'administrador': {'email': 'vtacius', 'password': 'vtacius'},
            'tecnicosuperior': {'email': 'alortiz', 'password': 'alortiz'},
            'usuario': {'email': 'usuario', 'password': 'usuario'}
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
