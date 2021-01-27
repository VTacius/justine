# justine
Una API REST para acceder a la administración de usuarios y grupos en en Samba4

## Desarrollo
```bash
apt install pipenv git curl jq
git clone git@github.com:VTacius/justine-api.git
cd justine-api
python setup.py develop
```

+ Creamos dos usuarios y un grupo que usaremos en las pruebas automatizadas
```bash
samba-tool group add http_access --nis-domain=DOMINIO.COM --gid-number=1001 --description "Grupos para acceso web"
samba-tool user create alortiz P.4ssw0rd --nis-domain=DOMINIO.COM --unix-home=/home/alortiz --uid-number=1002 --login-shell=/bin/false --gid-number=1001
samba-tool user create opineda P.4ssw0rd --nis-domain=DOMINIO.COM --unix-home=/home/opineda --uid-number=1003 --login-shell=/bin/false --gid-number=1001
```

## Administración desde consola

+ Obtenemos el token con el que vamos a realizar todas las demás operaciones
```bash
curl -s -L -XPOST -H 'Content-Type: application/json' 127.0.0.1:6543/auth/tokenizador --user alortiz -d '{"direccion": "alortiz", "rol": "administrador"}' | jq '.token'
```

### Usuarios

+ Listamos los usuarios disponibles en el directorio
```bash
curl -s -L XGET -H 'Content-Type: application/json' -H "www-authorization: $TOKEN" 127.0.0.1:6543/usuarios | jq
```

+ Creamos un usuario
```bash
curl -s -L -XPOST -H 'Content-Type: application/json' -H "www-authorization: $TOKEN" 127.0.0.1:6543/usuarios -d @datos.d/usuario_creacion.json | jq
```

+ Obtenemos los datos del usuario que acabamos de crear
```bash
curl -s -L -XGET -H 'Content-Type: application/json' -H "www-authorization: $TOKEN" 127.0.0.1:6543/usuarios/kpenate  | jq
```

+ Cambiamos el apellido a su forma correcta
```bash
curl -s -L -XPUT -H 'Content-Type: application/json' -H "www-authorization: $TOKEN" 127.0.0.1:6543/usuarios/kpenate -d @datos.d/usuario_modificacion.json
```

+ Borramos el usuario recién creado
```bash
curl -s -L -XDELETE -H 'Content-Type: application/json' -H "www-authorization: $TOKEN" 127.0.0.1:6543/usuarios/kpenate | jq
```

### Grupos

+ Listamos los grupos disponibles en el directorio
```bash
curl -s -L XGET -H 'Content-Type: application/json' -H "www-authorization: $TOKEN" 127.0.0.1:6543/grupos | jq
```

+ Creamos un grupo
```bash
curl -s -L -XPOST -H 'Content-Type: application/json' -H "www-authorization: $TOKEN" 127.0.0.1:6543/grupos -d @datos.d/grupo_creacion.json | jq
```

+ Obtenemos los datos del grupo recién creado
```bash
curl -s -L -XGET -H 'Content-Type: application/json' -H "www-authorization: $TOKEN" 127.0.0.1:6543/grupos/unidad | jq
```

+ Cambiamos la lista de correo asociada a la unidad
TODO: Falta implementar esto

+ Borramos el grupo recién creado
```bash
curl -s -L -XDELETE -H 'Content-Type: application/json' -H "www-authorization: $TOKEN" 127.0.0.1:6543/grupos/unidad
```
