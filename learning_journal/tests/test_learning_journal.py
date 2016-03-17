from learning_journal.models import Entry


def test_entry_creation(session):
    test_entry = Entry(title=u"Test Entry", text=u"Here is my test entry")
    session.add(test_entry)
    session.flush()
    assert session.query(Entry).filter(Entry.title==u"Test Entry")


def test_list_view(app, session, one_entry):
    #test_entry = Entry(title=u"Test Entry", text=u"Here is my test entry")
    #session.add(test_entry)
    #session.flush()
    response = app.get('/')
    assert response.status_code == 200
    actual = response.body
    assert one_entry.title in actual
    assert one_entry.text in actual
