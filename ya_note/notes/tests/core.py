from collections import namedtuple

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

USER_MODEL = get_user_model()
AUTHOR = 'Автор'
AUTH_USER = 'Авторизированный пользователь'

URL_NAME_IN_VIEWS = namedtuple(
    'NAME', (
        'home',
        'login',
        'logout',
        'signup',
    )
)

URL = URL_NAME_IN_VIEWS(
    reverse('notes:home'),
    reverse('users:login'),
    reverse('users:logout'),
    reverse('users:signup'),
)


class CoreTestCase(TestCase):
    """Создание объектов для тестов."""

    @classmethod
    def setUpTestData(cls):
        cls.author = USER_MODEL.objects.create(username='AUTHOR')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст заметки',
            slug='note-slug',
            author=cls.author
        )
