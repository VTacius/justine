# coding: utf-8

from pyramid.view import view_config

@view_config(route_name='home', renderer='json')
def get_actividad_list(request):
    return {'home': 'Comienzo'}
