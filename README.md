# justine
Una especie de API para acceder a la administración de usuarios en Samba y Zimbra

## Desarrollo
apt update
apt install virtualenv
virtualenv ambiente-justine
cd ambiente-justine/
git clone git@github.com:VTacius/justine-api.git

source bin/activate
pip install pyramid

ln -s /usr/lib/python2.7/dist-packages/Crypto/ /root/ambiente-justine/local/lib/python2.7/site-packages/
ln -s /usr/lib/python2.7/dist-packages/samba/ ~/ambiente-justine/lib/python2.7/
ln -s /usr/lib/python2.7/dist-packages/talloc.x86_64-linux-gnu.so ~/ambiente-justine/lib/python2.7/
ln -s /usr/lib/python2.7/dist-packages/ldb.so ~/ambiente-justine/lib/python2.7/

python setup.py develop

## Sobre como manejarlo desde consola


### Obtenemos el token
curl -H 'Content-Type: application/json' -XPOST http://0.0.0.0:6543/auth/login -d '{"usuario": "vtacius", "password": "vtacius"}' | jq '.token'

### Creamos el usuario
curl -s -L -XPOST -H 'Content-Type: application/json' -H "www-authorization: $TOKEN" 127.0.0.1:6543/usuarios -d @usuarioCreacion.json | jq

### Obtenemos los datos del usuario que acabamos de crear
curl -s -L -XGET -H 'Content-Type: application/json' -H "www-authorization: $TOKEN" 127.0.0.1:6543/usuarios/kpenate  | jq
