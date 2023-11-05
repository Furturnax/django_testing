import pytest
from datetime import datetime, timedelta
from collections import namedtuple

from django.conf import settings
from django.urls import reverse
from django.utils.timezone import now
from pytest_lazyfixture import lazy_fixture

from news.models import News, Comment

AUTHOR = 'Автор публикации'
PK = 1
CLIENT_USER = lazy_fixture('client')
AUTHOR_USER = lazy_fixture('author_client')
ADMIN_USER = lazy_fixture('admin_client')


URL_NAME_IN_VIEWS = namedtuple(
    'NAME', (
        'home',
        'login',
        'logout',
        'signup',
        'detail',
        'edit',
        'delete',
    )
)
URL = URL_NAME_IN_VIEWS(
    reverse('news:home'),
    reverse('users:login'),
    reverse('users:logout'),
    reverse('users:signup'),
    reverse('news:detail', args=(PK,)),
    reverse('news:edit', args=(PK,)),
    reverse('news:delete', args=(PK,)),
)


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username=AUTHOR)


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def news():
    return News.objects.create(
        title='Заголовок',
        text='Текст',
    )


@pytest.fixture
def comment(author, news):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Комментарий',
    )


@pytest.fixture
def pk_for_args(news):
    return news.pk,


@pytest.fixture
def news_list():
    return News.objects.bulk_create(
        News(
            title=f'Заголовок {index}',
            text='Текст',
            date=datetime.today().date() - timedelta(days=index),
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def comment_list(author, news):
    for index in range(2):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text='Комментарий',
        )
        comment.created = now + timedelta(days=index)
        comment.save()
    return comment_list


@pytest.fixture
def form_data():
    return {'text': 'Новый комментарий'}
