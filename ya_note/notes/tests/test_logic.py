from notes.models import Note
from notes.tests.core import CoreCheckData, URL


class TestAddNote(CoreCheckData):
    """Тест на создание заметок."""

    def test_user_can_create_note(self):
        """Тест создания заметки авторизированным пользователем."""
        expected_count = Note.objects.count() + 1
        self.assertRedirects(
            self.author_client.post(URL.add, data=self.form_data),
            URL.success,
            msg_prefix=('Проверьте, что после создания заметки '
                        'авторизированным пользователем произошёл '
                        f'редирект на страницу "{URL.success}".')
        )
        super().equal(expected_count)
        super().check_data(self.field_data)

    def test_anonymous_user_cant_create_note(self):
        """Тест создания заметки авторизированным пользователем."""
        expected_count = Note.objects.count()
        expected_url = f'{URL.login}?next={URL.add}'
        self.assertRedirects(
            self.client.post(URL.add, data=self.form_data),
            expected_url,
            msg_prefix=('Проверьте, что при создания заметки анонимным '
                        'пользователем произошёл редирект на '
                        f'страницу "{URL.login}".')
        )
        super().equal(expected_count)

#     def test_not_unique_slug():
#         pass

#     def test_empty_slug():
#         pass


# class TestEditDeleteNote(CoreCheckData):

#     def test_author_can_edit_note():
#         pass

#     def test_other_user_cant_edit_note():
#         pass

#     def test_author_can_delete_note():
#         pass

#     def test_other_user_cant_delete_note():
#         pass
