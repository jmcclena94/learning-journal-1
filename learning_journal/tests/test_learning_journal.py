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
    test_entry = session.query(Entry).filter(Entry.title == u"Test Entry"
                                             ).first()
    url = '/entry/{id}'.format(id=test_entry.id)
    response = app.get(url)
    assert test_entry.title in response.text
    assert test_entry.text in response.text


def test_add_entry_view(app, session):
    url = '/entry/add'
    response = app.get(url)
    assert response.status_code == 200
    assert '<form method="POST">' in response.text
    app.post(url, {'title': 'Add Test', 'text': 'new text'})
    assert session.query(Entry).filter(Entry.title == u"Add Test").first()


def test_edit_entry_view(app, session):
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


# def test_no_access_to_view(app):
#     response = app.get('/secure', status=403)
#     assert response.status_code == 403
#
#
# def test_password_exist(app, auth_env):
#     assert os.environ.get('AUTH_PASSWORD') is not None
#
#
# def test_username_exist(app, auth_env):
#     assert os.environ.get('AUTH_USERNAME') is not None
#
#
# def test_check_pw_success(auth_env):
#     from .security import check_pw
#     password = 'secret'
#     assert check_pw(password)
#
#
# def test_stored_password_is_encrypted(auth_env):
#     assert os.environ.get('AUTH_PASSWORD') != 'secret'
#
#
# def test_check_ps_fails(auth_env):
#     from .security import check_pw
#     password = 'notsecret'
#     assert not check_pw(password)
#
#
# def test_post_login_success(app, authenv):
#     data = {'username': 'admin', 'password': 'secret'}
#     response = app.post('/login', data)
#     assert response.status_code == 200
#
#
# def test_post_login_success_auth_tkt_present(app, auth_env):
#     data = {'username': 'admin', 'password': 'secret'}
#     response = app.post('/login', data)
#     headers = response.headers
#     cookies_set = headers.getall('Set-Cookie')
#     assert cookies_set
#     for cookie in cookies_set:
#         if cookie.startswith('auth_tkt'):
#             break
#     else:
#         assert False
