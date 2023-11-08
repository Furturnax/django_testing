from datetime import date

import pytest
from django.conf import settings
from django.utils.timezone import datetime

from news.forms import CommentForm

pytestmark = pytest.mark.django_db


def test_count_news_on_homepage_and_news_order(client, news_list, urls):
    """Тест количества новостей на главной странице и их порядок по дате."""
    object_list = list(
        client.get(urls.home).context['object_list']
    )
    assert len(object_list) == settings.NEWS_COUNT_ON_HOME_PAGE, (
        f'Проверьте, что на странице "{urls.home}" количество '
        f'новостей {settings.NEWS_COUNT_ON_HOME_PAGE}'
    )
    assert isinstance(object_list[0].date, date), (
        'Проверьте, что дата публикации объект типа "date".'
    )
    assert object_list == sorted(
        object_list, key=lambda news: news.date, reverse=True
    ), ('Проверьте, что список новостей отсортирован по полю "date" '
        'от нового к старому.')


def test_comment_order(client, comments_list, urls):
    """Тест сортировки комментариев."""
    assert 'news' in client.get(urls.detail).context, (
        'Проверьте, что в контексте ответа есть переменная "news".'
    )
    all_comments = list(
        client.get(urls.detail).context['news'].comment_set.all()
    )
    assert isinstance(all_comments[0].created, datetime), (
        'Проверьте, что дата и время комментария объект типа "datetime".'
    )
    assert all_comments == sorted(
        all_comments, key=lambda comment: comment.created, reverse=False
    ), ('Проверьте, что список комментариев отсортирован по полю "created" '
        'от старого к новому.')


@pytest.mark.parametrize('client_type', ('anonymous', 'admin'))
def test_anonymous_user_havent_form_for_comments(
        client, admin_client, news, urls, client_type
):
    """Тест отправки формы комментария анонимному пользователю."""
    if client_type == 'anonymous':
        response = client.get(urls.detail)
        expected_message = (
            'Проверьте, что для анонимного пользователя недоступна '
            'форма для отправки комментариев.')
    elif client_type == 'admin':
        response = admin_client.get(urls.detail)
        expected_message = (
            'Проверьте, что для авторизованного пользователя доступна '
            'форма для отправки комментариев.')
    assert ('form' in response.context) == (client_type == 'admin'), (
        expected_message)
    assert isinstance(
        admin_client.get(urls.detail).context['form'], CommentForm
    ), ('Проверьте, что форма для авторизированного пользователя является '
        'экземпляром CommentForm.')
