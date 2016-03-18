from learning_journal.models import Entry


def test_entry_creation(session):
    test_entry = Entry(title=u"Test Entry", text=u"Here is my test entry")
    session.add(test_entry)
    session.flush()
    assert session.query(Entry).filter(Entry.title==u"Test Entry")


def test_list_view(app, one_entry):
    response = app.get('/')
    assert response.status_code == 200
    actual = response.body
    assert one_entry.title.encode('utf8') in actual


def test_entry_view(app, session):
    test_entry = session.query(Entry).filter(Entry.title==u"Test Entry").first()
    url = '/entry/{id}'.format(id=test_entry.id)
    response = app.get(url)
    assert test_entry.title.encode('utf8') in response.body
    assert test_entry.text.encode('utf8') in response.body

def test_add_entry_view(app, session):
    url = '/add_entry'
    response = app.get(url)
    assert response.status_code == 200
    assert b'<form method="POST">' in response.body
    app.post(url, {'title': 'Add Test', 'text': 'new text'})
    assert session.query(Entry).filter(Entry.title==u"Add Test").first()


def test_edit_entry_view(app, session):
    one_entry = session.query(Entry).filter(Entry.title==u"Test Entry").first()
    url = '/entry/{id}/edit'.format(id=one_entry.id)
    response = app.get(url)
    assert response.status_code == 200
    starting_page = response.body
    assert one_entry.title.encode('utf8') in starting_page
    assert one_entry.text.encode('utf8') in starting_page
    app.post(url, {'title': "New Title", 'text': 'new text'})
    edited_response = app.get(url)
    assert edited_response.status_code == 200
    edited_page = edited_response.body
    assert b"New Title" in edited_page
    assert b"new text" in edited_page
