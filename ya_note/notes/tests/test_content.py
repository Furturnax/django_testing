from notes.forms import NoteForm
from notes.tests.core import CoreTestCase, URL


class TestNotesList(CoreTestCase):
    """Тест на создание, редактирование и видимость контента."""

    def test_user_notes_not_visible_to_other_users(self):
        """Тест видимости своих заметок в своём списке."""
        clients = (
            (URL.list, self.author_client, True),
            (URL.list, self.user_client, False),
        )
        for url, client, arg in clients:
            with self.subTest(url=url, client=client, arg=arg):
                object_list = client.get(url).context['object_list']
                self.assertTrue(
                    (self.note in object_list) is arg,
                    msg=(f'Проверьте, что {client} не видит чужие заметки '
                         'в списке своих заметок.'),
                )

    def test_get_forms_on_add_or_edit_pages_from_author(self):
        """Тест передачи формы для создания и редактирования заметок."""
        urls = (
            (URL.add),
            (URL.edit),
        )
        for url in urls:
            with self.subTest(url=url, client=self.author_client):
                self.assertIsInstance(
                    self.author_client.get(url).context['form'],
                    NoteForm,
                    msg=('Проверьте, что форма для создания или '
                         'редактирования заметки передается '
                         f'на страницу "{url}"'),
                )
