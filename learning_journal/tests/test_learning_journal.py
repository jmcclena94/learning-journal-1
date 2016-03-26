from learning_journal.models import Entry
import os


def test_entry_creation(session):
    test_entry = Entry(title=u"Test Entry", text=u"Here is my test entry")
    session.add(test_entry)
    session.flush()
    assert session.query(Entry).filter(Entry.title == u"Test Entry")


def test_list_view(app, one_entry):
    response = app.get('/')
    assert response.status_code == 200
    actual = response.text
    assert one_entry.title in actual


def test_entry_view(app, session):
    app.post('/login', {
        'usrname': 'owner', 'pswd': os.environ.get('TEST_LJ_PW')})
    test_entry = session.query(Entry).filter(Entry.title == u"Test Entry"
                                             ).first()
    url = '/entry/{id}'.format(id=test_entry.id)
    response = app.get(url)
    assert test_entry.title in response.text
    assert test_entry.text in response.text


def test_add_entry_view(app, session):
    app.post('/login', {
        'usrname': 'owner', 'pswd': os.environ.get('TEST_LJ_PW')})
    url = '/entry/add'
    response = app.get(url)
    assert response.status_code == 200
    assert '<form class="flexbox entry-form" method="POST">' in response.text
    app.post(url, {'title': 'Add Test', 'text': 'new text'})
    assert session.query(Entry).filter(Entry.title == u"Add Test").first()


def test_edit_entry_view(app, session, auth_env):
    app.post('/login', {
        'usrname': 'owner', 'pswd': os.environ.get('TEST_LJ_PW')})
    one_entry = session.query(Entry).filter(Entry.title == u"Test Entry"
                                            ).first()
    url = '/entry/{id}/edit'.format(id=one_entry.id)
    response = app.get(url)
    assert response.status_code == 200
    starting_page = response.text
    assert one_entry.title in starting_page
    assert one_entry.text in starting_page
    app.post(url, {'title': "New Title", 'text': 'new text'})
    edited_response = app.get(url)
    assert edited_response.status_code == 200
    edited_page = edited_response.text
    assert "New Title" in edited_page
    assert "new text" in edited_page


def test_no_access_to_add_view(app):
    response = app.get('/entry/add', status=403)
    assert response.status_code == 403


def test_no_access_to_edit_view(app):
    response = app.get('/entry/1/edit', status=403)
    assert response.status_code == 403


def test_password_exist(app, auth_env):
    assert os.environ.get('AUTH_PASSWORD') is not None


def test_username_exist(app, auth_env):
    assert os.environ.get('AUTH_USERNAME') is not None


def test_stored_password_is_encrypted(auth_env):
    assert os.environ.get('AUTH_PASSWORD') != 'secret'


def test_login_view_good(app, auth_env, session):
    url = '/login'
    response = app.post(url, {
        'usrname': 'owner', 'pswd': os.environ.get('TEST_LJ_PW')})
    assert response.status_code == 302


def test_login_view_bad(app, auth_env, session):
    url = '/login'
    response = app.post(url, {'usrname': 'owner', 'pswd': 'bad'}, status=403)
    assert response.status_code == 403


def test_logout_view(app, session):
    response = app.get('/logout')
    assert response.status_code == 302
