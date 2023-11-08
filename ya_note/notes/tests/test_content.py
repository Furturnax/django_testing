from notes.forms import NoteForm
from notes.models import Note
from notes.tests.core import CoreTestCase, URL


class TestNotesList(CoreTestCase):
    """Тест на создание, редактирование и видимость контента."""

    def test_user_notes_visible_to_author(self):
        """Тест видимости своих заметок автором в списке заметок."""
        expected_count = Note.objects.count()
        object_list = self.author_client.get(URL.list).context['object_list']
        self.assertEqual(
            len(object_list),
            expected_count,
            msg=('Проверьте, что в списке заметок одна заметка.'),
        )
        self.assertEqual(
            self.note.title,
            'Заголовок',
            msg=('Проверьте, что заголовок совпадает с заголовком в БД.'),
        )
        self.assertEqual(
            self.note.text,
            'Текст заметки',
            msg=('Проверьте, что текст совпадает с текстом в БД.'),
        )

    def test_user_notes_not_visible_to_not_author(self):
        """Тест видимости чужих заметок не автором в списке заметок."""
        expected_count = Note.objects.count() - 1
        object_list = self.user_client.get(URL.list).context['object_list']
        self.assertEqual(
            len(object_list),
            expected_count,
            msg=('Проверьте, что в списке заметок нет заметок'),
        )

    def test_get_forms_on_add_or_edit_pages_from_author(self):
        """Тест передачи формы для создания и редактирования заметок."""
        urls = (
            (URL.add),
            (URL.edit),
        )
        for url in urls:
            with self.subTest(url=url, client=self.author_client):
                form = self.author_client.get(url)
                self.assertIn(
                    'form',
                    form.context,
                    msg=('Проверьте, что форма заметки передаётся на '
                         f'страницу "{url}".')
                )
                self.assertIsInstance(
                    form.context['form'],
                    NoteForm,
                    msg=('Проверьте, что форма для создания или '
                         'редактирования заметки является '
                         'экземпляром класса "NoteForm".'),
                )
