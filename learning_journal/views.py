# from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from passlib.hash import sha256_crypt

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc

import os

from .models import (
    DBSession,
    Entry,
    )

from wtforms import Form, StringField, TextAreaField, PasswordField, validators

# from .security import check_pw


class EntryForm(Form):
    title = StringField(u'Title', [validators.required(),
                        validators.length(max=128)])
    text = TextAreaField(u'Entry', [validators.required()])


class LoginForm(Form):
    usrname = StringField(u'User Name', [validators.required()])
    pswd = PasswordField(u'Password', [validators.required()])


@view_config(route_name='login', renderer='templates/login.jinja2',
             permission='read')
def login_view(request):
    """Login page view."""
    login_form = LoginForm(request.POST)
    if request.method == 'POST' and login_form.validate():
        usrname = login_form.usrname.data
        pswd = login_form.pswd.data
        usrcheck = usrname == 'owner'
        pwdcheck = sha256_crypt.verify(pswd, os.environ.get('LJ_AUTH'))
        if usrcheck and pwdcheck:
            headers = remember(request, usrname)
            return HTTPFound(request.route_url('list'), headers=headers)
        return HTTPFound(request.route_url('login'))
    return {'title': 'Login', 'form': login_form}


@view_config(route_name='list', renderer='templates/list_template.jinja2',
             permission='read')
def list_view(request):
    entries = DBSession.query(Entry).order_by(desc(Entry.created))
    return {'entries': entries, 'title': 'Learning Journal'}


@view_config(route_name='detail', renderer='templates/detail_template.jinja2',
             permission='read')
def detail_view(request):
    id = request.matchdict['id']
    entry = DBSession.query(Entry).filter(
        Entry.id == id).first()
    title = "Learning Journal Entry {}".format(id)
    return {'entry': entry, 'entry_text': entry.markdown(), 'title': title}


@view_config(route_name='add_entry',
             renderer='templates/add_entry_template.jinja2',
             permission='create')
def add_entry_view(request):
    entry_form = EntryForm(request.POST)
    if request.method == 'POST' and entry_form.validate():
        try:
            new_entry = Entry(title=entry_form.title.data,
                              text=entry_form.text.data)
            DBSession.add(new_entry)
        except SQLAlchemyError:
            return {'title': 'Add Entry', 'form': entry_form,
                    'error': 'Title Already Used'}
        return HTTPFound(request.route_url('list'))
    return {'title': 'Add Entry', 'form': entry_form}


@view_config(route_name='edit_entry',
             renderer='templates/edit_entry_template.jinja2',
             permission='edit')
def edit_entry_view(request):
    id = request.matchdict['id']
    current_entry = DBSession.query(Entry).filter(Entry.id == id).first()
    edited_form = EntryForm(request.POST, current_entry)
    if request.method == 'POST' and edited_form.validate():
        current_entry.title = edited_form.title.data
        current_entry.text = edited_form.text.data
        return HTTPFound(location='/entry/{id}'.format(id=id))
    return {'title': 'Add Entry', 'form': edited_form}


@view_config(route_name='logout')
def logout_view(request):
    """Logout."""
    headers = forget(request)
    return HTTPFound(request.route_url('list'), headers=headers)


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_learning-journal_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
