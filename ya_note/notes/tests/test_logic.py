from notes.tests.core import CoreTestCase


class TestAddNote(CoreTestCase):

    def test_user_can_create_note():
        pass

    def test_anonymous_user_cant_create_note():
        pass

    def test_not_unique_slug():
        pass

    def test_empty_slug():
        pass


class TestEditDeleteNote(CoreTestCase):

    def test_author_can_edit_note():
        pass

    def test_other_user_cant_edit_note():
        pass

    def test_author_can_delete_note():
        pass

    def test_other_user_cant_delete_note():
        pass
