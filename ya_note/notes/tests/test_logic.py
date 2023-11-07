from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from notes.tests.core import (
    CoreCheckData,
    CoreTestCase,
    FIELD_FORM,
    NEW_FORM_DATA,
    SLUG,
    URL
)


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
        note = Note.objects.first()
        super().comparison_count_notes_in_db(expected_count)
        super().check_data_from_form_and_db(note, self.field_data)

    def test_anonymous_user_cant_create_note(self):
        """Тест создания заметки не авторизированным пользователем."""
        expected_count = Note.objects.count()
        expected_url = f'{URL.login}?next={URL.add}'
        self.assertRedirects(
            self.client.post(URL.add, data=self.form_data),
            expected_url,
            msg_prefix=('Проверьте, что при создании заметки анонимным '
                        'пользователем произошёл редирект на '
                        f'страницу "{URL.login}".')
        )
        super().comparison_count_notes_in_db(expected_count)

    def test_not_unique_slug(self):
        """Тест на невозможность создания заметок с одинаковым slug."""
        expected_count = Note.objects.count() + 1
        Note.objects.create(**dict(zip(FIELD_FORM, self.field_data)))
        self.assertFormError(
            self.author_client.post(URL.add, data=self.form_data),
            form='form',
            field='slug',
            errors=(SLUG + WARNING),
            msg_prefix=('Проверьте, что при создании заметки с '
                        'существующим slug в форме возникает '
                        f'ошибка "{WARNING}".')
        )
        super().comparison_count_notes_in_db(expected_count)

    def test_empty_slug(self):
        """Тест на автоматическое создание slug."""
        expected_count = Note.objects.count() + 1
        self.form_data.pop('slug')
        self.assertRedirects(
            self.author_client.post(URL.add, data=self.form_data),
            URL.success,
            msg_prefix=('Проверьте, что после создания заметки '
                        'авторизированным пользователем произошёл '
                        f'редирект на страницу "{URL.success}".')
        )
        note = Note.objects.get()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(
            note.slug,
            expected_slug,
            msg=('Проверьте, что автоматически созданный slug '
                 'соответствует ожидаемому.')
        )
        super().comparison_count_notes_in_db(expected_count)


class TestEditDeleteNote(CoreTestCase, CoreCheckData):
    """Тест на редактирование или удаление заметки."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.new_form_data = dict(zip(FIELD_FORM, NEW_FORM_DATA))

    def test_author_can_edit_note(self):
        """Тест на редактирование заметки автором."""
        self.assertRedirects(
            self.author_client.post(URL.edit, data=self.new_form_data),
            URL.success,
            msg_prefix=('Проверьте, что после редактирования заметки '
                        f'произошёл редирект на страницу "{URL.success}".')
        )
        note = Note.objects.first()
        super().check_data_from_form_and_db(note, self.new_field_data)

    def test_other_user_cant_edit_note(self):
        """Тест на редактирование заметки не автором."""
        self.assertEqual(
            self.user_client.post(URL.edit,
                                  data=self.new_form_data).status_code,
            HTTPStatus.NOT_FOUND,
            msg=('Проверьте, что при редактировании не своей заметки '
                 'произошёл редирект на страницу с ошибкой 404.')
        )
        note = Note.objects.first()
        super().check_data_from_form_and_db(note, self.field_data)

    def test_author_can_delete_note(self):
        """Тест на удаление заметки автором."""
        expected_count = Note.objects.count() - 1
        self.assertRedirects(
            self.author_client.post(URL.delete),
            URL.success,
            msg_prefix=('Проверьте, что после удаления заметки '
                        f'произошёл редирект на страницу "{URL.success}".')
        )
        super().comparison_count_notes_in_db(expected_count)

    def test_other_user_cant_delete_note(self):
        """Тест на удаление заметки не автором."""
        expected_count = Note.objects.count()
        self.assertEqual(
            self.user_client.post(URL.delete).status_code,
            HTTPStatus.NOT_FOUND,
            msg=('Проверьте, что при удалении не своей заметки '
                 'произошёл редирект на страницу с ошибкой 404.')
        )
        super().comparison_count_notes_in_db(expected_count)
