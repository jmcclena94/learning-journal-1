from learning_journal.models import Entry


def test_entry_creation(session):
    test_entry = Entry(title=u"Test Entry", text=u"Here is my test entry")
    session.add(test_entry)
    session.flush()
    assert session.query(Entry).filter(Entry.title==u"Test Entry")
    session.close()


def test_entry_render(dbtransaction, session):
    test_entry = Entry(title=u"Test Entry1", text=u"Here is my test entry1")
    session.add(test_entry)
    session.flush()
