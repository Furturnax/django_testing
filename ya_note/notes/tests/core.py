from collections import namedtuple

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

USER_MODEL = get_user_model()
AUTHOR = 'Автор публикации'
AUTH_USER = 'Авторизованный пользователь'
SLUG = 'note-slug'
NEW_SLUG = 'new-slug'
FIELD_FORM = ('title', 'text', 'slug', 'author')
FORM_DATA = ('Заголовок', 'Текст заметки', SLUG)
NEW_FORM_DATA = ('Новый заголовок', 'Новый текст заметки', NEW_SLUG)
URL_NAME_IN_VIEWS = namedtuple(
    'NAME', (
        'home',
        'login',
        'logout',
        'signup',
        'add',
        'success',
        'list',
        'detail',
        'edit',
        'delete',
    )
)
URL = URL_NAME_IN_VIEWS(
    reverse('notes:home'),
    reverse('users:login'),
    reverse('users:logout'),
    reverse('users:signup'),
    reverse('notes:add'),
    reverse('notes:success'),
    reverse('notes:list'),
    reverse('notes:detail', args=(SLUG,)),
    reverse('notes:edit', args=(SLUG,)),
    reverse('notes:delete', args=(SLUG,)),
)


class CoreTestCase(TestCase):
    """Создание объектов в БД для проверки."""

    @classmethod
    def setUpTestData(cls):
        cls.author = USER_MODEL.objects.create(username=AUTHOR)
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.user = USER_MODEL.objects.create(username=AUTH_USER)
        cls.user_client = Client()
        cls.user_client.force_login(cls.user)
        cls.note = Note.objects.create(
            **dict(zip(FIELD_FORM, (*FORM_DATA, cls.author)))
        )


class CoreCheckData(TestCase):
    """Создание и сопоставление объектов в БД."""

    @classmethod
    def setUpTestData(cls):
        cls.author = USER_MODEL.objects.create(username=AUTHOR)
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.form_data = dict(zip(FIELD_FORM, FORM_DATA))
        cls.field_data = (*FORM_DATA, cls.author)

    def check_data_from_form_and_db(self, field_data):
        """Сравнение данных отправленных в форме с данными в БД."""
        note = Note.objects.get()
        data_from_db = (note.title, note.text, note.slug, note.author)
        for sent_value, db_value in zip(field_data, data_from_db):
            with self.subTest(sent_value=sent_value, db_value=db_value):
                self.assertEqual(
                    sent_value,
                    db_value,
                    msg=(
                        'Проверьте, что в базу данных добавлена запись, '
                        'которая совпадает с той, что отправлена из формы.'
                    ),
                )

    def comparison_count_notes_in_db(self, expected_count):
        """Сопоставление количества заметок в БД после любого действия."""
        notes_count = Note.objects.count()
        self.assertEqual(
            expected_count,
            notes_count,
            msg=(
                'Проверьте, что количество записей в БД соответствует '
                'ожидаемому.'
            ),
        )
