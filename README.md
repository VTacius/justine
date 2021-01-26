# justine
Una especie de API para acceder a la administración de usuarios en Samba y Zimbra

## Desarrollo
```bash
apt install pipenv git curl jq
git clone git@github.com:VTacius/justine-api.git
cd justine-api
pipenv --python 3.7 shell
python setup.py develop
```

### Creamos un par de usuario
```bash
samba-tool group add http_access --nis-domain=DOMINIO.COM --gid-number=1001 --description "Grupos para acceso web"
samba-tool user create alortiz P.4ssw0rd --nis-domain=DOMINIO.COM --unix-home=/home/alortiz --uid-number=1002 --login-shell=/bin/false --gid-number=1001
samba-tool user create opineda P.4ssw0rd --nis-domain=DOMINIO.COM --unix-home=/home/opineda --uid-number=1003 --login-shell=/bin/false --gid-number=1001
```

### Obtenemos el token con el que vamos a realizar todas las demás operaciones
```bash
curl -s -L -XPOST -H 'Content-Type: application/json' 127.0.0.1:6543/auth/tokenizador --user alortiz -d '{"direccion": "alortiz", "rol": "administrador"}' | jq '.token'
```

### Creamos el usuario
```bash
curl -s -L -XPOST -H 'Content-Type: application/json' -H "www-authorization: $TOKEN" 127.0.0.1:6543/usuarios -d @usuarioCreacion.json | jq
```

### Obtenemos los datos del usuario que acabamos de crear
```bash
curl -s -L -XGET -H 'Content-Type: application/json' -H "www-authorization: $TOKEN" 127.0.0.1:6543/usuarios/kpenate  | jq
```
