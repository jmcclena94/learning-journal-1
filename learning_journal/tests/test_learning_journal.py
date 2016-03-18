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
    assert one_entry.title in actual


def test_edit_entry_view(app, one_entry):
    url = '/entry/{id}/edit'.format(id=one_entry.id)
    response = app.get(url)
    assert response.status_code == 200
    starting_page = response.body
    assert one_entry.title in starting_page
    assert one_entry.text in starting_page
    app.post(url, {'title': "New Title", 'text': 'new text'})
    edited_response = app.get(url)
    assert edited_response.status_code == 200
    edited_page = edited_response.body
    assert "New Title" in edited_page
    assert "new text" in edited_page
