import os
from passlib.apps import custom_app_context as pwd_context
from pyramid.security import Allow, Everyone


def check_pw(pw):
    hashed = os.environ.get('AUTH_PASSWORD', 'wrong')
    return pwd_context.verify(pw, hashed)


class MyRoot(object):
    __acl__ = [
        (Allow, Authenticated, 'gonzo')
        (Allow, Everyone, 'view')
    ]

    def __init__(self, request):
        self.request = request
