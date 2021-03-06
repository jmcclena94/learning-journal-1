from pyramid.config import Configurator
from sqlalchemy import engine_from_config
import os
from .security import MyRoot

from .models import (
    DBSession,
    Base,
    )
# from .security import DefaultRoot, groupfinder

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

# from pyramid.session import SignedCookieSessionFactory


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    auth_secret = os.environ.get('LJ_AUTH')
    authentication_policy = AuthTktAuthenticationPolicy(
        secret=auth_secret,
        hashalg='sha512',
    )
    authorization_policy = ACLAuthorizationPolicy()

    config = Configurator(
        settings=settings,
        root_factory=MyRoot,
        )

    config.set_authentication_policy(authentication_policy)
    config.set_authorization_policy(authorization_policy)

    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('login', '/login')
    config.add_route('list', '/')
    config.add_route('detail', '/entry/{id:\d+}')
    config.add_route('add_entry', '/entry/add')
    config.add_route('edit_entry', '/entry/{id}/edit')
    config.add_route('logout', '/logout')
    config.scan()
    return config.make_wsgi_app()
