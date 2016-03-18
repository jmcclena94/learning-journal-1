from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from sqlalchemy.exc import DBAPIError
from sqlalchemy import desc

from .models import (
    DBSession,
    Entry,
    )

from wtforms import Form, StringField, TextAreaField, validators
import markdown

class EntryForm(Form):
    title = StringField(u'Title', [validators.required(),
                        validators.length(max=128)])
    text = TextAreaField(u'Entry', [validators.required()])


@view_config(route_name='list', renderer='templates/list_template.jinja2')
def list_view(request):
    entries = DBSession.query(Entry).order_by(desc(Entry.created))
    return {'entries': entries, 'title': 'Learning Journal'}


@view_config(route_name='detail', renderer='templates/detail_template.jinja2')
def detail_view(request):
    entry = DBSession.query(Entry).filter(
        Entry.id == request.matchdict['id']).first()
    title = "Learning Journal Entry {}".format(request.matchdict['id'])
    return {'entry': entry, 'entry_text': markdown.markdown(entry.text), 'title': title}


@view_config(route_name='add_entry',
             renderer='templates/add_entry_template.jinja2')
def add_entry_view(request):
    entry_form = EntryForm(request.POST)
    if request.method == 'POST' and entry_form.validate():
        #import pdb; pdb.set_trace()
        new_entry = Entry(title=entry_form.title.data, text=entry_form.text.data)
        DBSession.add(new_entry)
        # TODO: redirect to the new entry
    return {'title': 'Add Entry', 'form': entry_form}


@view_config(route_name='edit_entry',
             renderer='templates/edit_entry_template.jinja2')
def edit_entry_view(request):
    current_entry = DBSession.query(Entry).filter(
        Entry.id == request.matchdict['id']).first()
    entry_form = EntryForm(request.GET, current_entry)
    edited_form = EntryForm(request.POST)
    if request.method == 'POST' and edited_form.validate():
        current_entry.title = edited_form.title.data
        current_entry.text = edited_form.text.data
        return HTTPFound(location='/entry/{id}'.format(
            id=request.matchdict['id']))
    entry_form.populate_obj(current_entry)
    return {'title': 'Add Entry', 'form': entry_form}


# @view_config(route_name='home', renderer='templates/mytemplate.pt')
# def my_view(request):
#     try:
#         one = DBSession.query(Entry).filter(Entry.name == 'one').first()
#     except DBAPIError:
#         return Response(conn_err_msg, content_type='text/plain', status_int=500)
#     return {'one': one, 'project': 'learning-journal'}


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
