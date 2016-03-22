import os
from passlib.apps import custom_app_context as pwd_context


def check_pw(pw):
    hashed = os.environ.get('AUTH_PASSWORD', 'wrong')
    return pwd_context.verify(pw, hashed)
