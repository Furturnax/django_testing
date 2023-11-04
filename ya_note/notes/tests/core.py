from collections import namedtuple

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

USER_MODEL = get_user_model()
AUTHOR = 'Автор'
AUTH_USER = 'Авторизированный пользователь'
SLUG = 'note-slug'

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
    """Создание объектов для тестов."""

    @classmethod
    def setUpTestData(cls):
        cls.author = USER_MODEL.objects.create(username='AUTHOR')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.user = USER_MODEL.objects.create(username='AUTH_USER')
        cls.user_client = Client()
        cls.user_client.force_login(cls.user)
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст заметки',
            slug=SLUG,
            author=cls.author
        )
