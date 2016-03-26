from pyramid.security import Allow, Everyone, Authenticated


class MyRoot(object):
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, 'create'),
        (Allow, Authenticated, 'edit'),
    ]

    def __init__(self, request):
        self.request = request
