import pytest
from datetime import datetime, timedelta
from collections import namedtuple

from django.conf import settings
from django.urls import reverse
from django.utils.timezone import now
from pytest_lazyfixture import lazy_fixture

from news.models import News, Comment

PK = 1
ANONYM = lazy_fixture('client')
AUTHOR = lazy_fixture('author_client')
AUTH_USER = lazy_fixture('admin_client')
COMMENT_TEXT = 'Текст комментария'
NEW_COMMENT_TEXT = 'Новый комментарий'


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
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def news():
    return News.objects.create(
        title='Заголовок',
        text='Текст новости',
    )


@pytest.fixture
def comment(author, news):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария',
    )


@pytest.fixture
def pk_for_args(news):
    return (news.pk,)


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
def comments_list(author, news):
    for index in range(2):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text='Комментарий',
        )
        comment.created = now() + timedelta(days=index)
        comment.save()
    return comments_list


@pytest.fixture
def form_data():
    return {'text': 'Новый комментарий'}
