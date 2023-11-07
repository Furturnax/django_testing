from collections import namedtuple
from datetime import datetime, timedelta
from http import HTTPStatus

import pytest
from django.conf import settings
from django.urls import reverse
from django.utils.timezone import now
from pytest_lazyfixture import lazy_fixture

from news.models import News, Comment

ANONYM = lazy_fixture('client')
AUTHOR = lazy_fixture('author_client')
AUTH_USER = lazy_fixture('admin_client')
NEWS_TITLE = 'Заголовок'
NEWS_TEXT = 'Текст новости'
COMMENT_TEXT = 'Текст комментария'
COMMENT_TEXT_NEW = 'Новый комментарий'


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
        title=NEWS_TITLE,
        text=NEWS_TEXT,
    )


@pytest.fixture
def pk_for_args(news):
    return news.pk


@pytest.fixture
def comment(author, news):
    return Comment.objects.create(
        news=news,
        author=author,
        text=COMMENT_TEXT,
    )


@pytest.fixture
def news_list():
    return News.objects.bulk_create(
        News(
            title=f'Заголовок {index}',
            text=f'Текст {index}',
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
            text=COMMENT_TEXT,
        )
        comment.created = now() + timedelta(days=index)
        comment.save()
    return comments_list


@pytest.fixture
def form_data():
    return {'text': COMMENT_TEXT_NEW}


@pytest.fixture
def url_for_anonymous():
    return namedtuple(
        'Name',
        (
            'home',
            'login',
            'logout',
            'signup',
        )
    )(
        reverse('news:home'),
        reverse('users:login'),
        reverse('users:logout'),
        reverse('users:signup'),
    )


@pytest.fixture
def url_for_user(pk_for_args):
    return namedtuple(
        'Name',
        (
            'detail',
        )
    )(
        reverse('news:detail', args=(pk_for_args,)),
    )


@pytest.fixture
def url_for_author(pk_for_args):
    return namedtuple(
        'Name',
        (
            'edit',
            'delete',
        )
    )(
        reverse('news:edit', args=(pk_for_args,)),
        reverse('news:delete', args=(pk_for_args,)),
    )


@pytest.fixture
def pages_for_anonymous(url_for_anonymous):
    return url_for_anonymous


@pytest.fixture
def pages_for_user(url_for_user):
    return url_for_user


@pytest.fixture
def pages_for_author(url_for_author):
    return url_for_author


@pytest.fixture
def urls(url_for_anonymous, url_for_user, url_for_author):
    return namedtuple(
        'Urls', (
            *url_for_anonymous._fields,
            *url_for_user._fields,
            *url_for_author._fields,
        )
    )(
        *url_for_anonymous,
        *url_for_user,
        *url_for_author,
    )


def comparison_count_comments_in_db(expected_count):
    """Сопоставление количества комментариев в БД после любого действия."""
    comments_count = Comment.objects.count()
    assert expected_count == comments_count, (
        'Проверьте, что авторизированный пользователь смог написать '
        'комментарий.'
    )


def return_status_404(response):
    """Возвращает статус ответа 404."""
    assert response.status_code == HTTPStatus.NOT_FOUND, (
        'Проверьте, что статус ответа 404.'
    )
