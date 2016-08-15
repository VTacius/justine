USERS = {'vtacius': 'editor', 'alortiz': 'viewer'}
GROUPS = {'vtacius': ['groups:editors', 'groups:admins']}

def groupfinder(userid, request):
    if userid in USERS:
        return GROUPS.get(userid, [])


