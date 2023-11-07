import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from conftest import (
    comparison_count_comments_in_db,
    return_status_404,
    COMMENT_TEXT,
    COMMENT_TEXT_NEW,
    URL
)
from news.forms import BAD_WORDS, WARNING
from news.models import Comment

pytestmark = pytest.mark.django_db


def test_anonymous_user_cant_create_comment(client, form_data):
    """Тест на создание комментария анонимным пользователем."""
    expected_count = Comment.objects.count()
    client.post(URL.detail, data=form_data)
    comparison_count_comments_in_db(expected_count)


def test_auth_user_can_create_comment(
        author, author_client, form_data, news
):
    """Тест на создание комментария авторизированным пользователем."""
    expected_count = Comment.objects.count() + 1
    comments_before = set(Comment.objects.all())
    assertRedirects(
        author_client.post(URL.detail, data=form_data),
        f'{URL.detail}#comments',
        msg_prefix=('Проверьте, что произошел редирект на страницу '
                    f'"{URL.detail}".'),
    )
    comments_after = set(Comment.objects.all())
    assert len(comments_after - comments_before) == 1, (
        'Проверьте, что разница между количеством коментариев до запроса '
        'и после запроса составляет "1".'
    )
    new_comment = (comments_after - comments_before).pop()
    assert new_comment.news == news, (
        'Проверьте, что новость связана с комментарием.'
    )
    assert new_comment.author == author, (
        'Проверьте, что автор комментария совпадает.'
    )
    assert new_comment.text == form_data['text'], (
        'Проверьте, что комментарий совпадает.'
    )
    comparison_count_comments_in_db(expected_count)


@pytest.mark.parametrize(
    'word',
    (BAD_WORDS),
)
def test_user_cant_use_bad_words_in_comments(author_client, word, news):
    """Тест на запрет написания плохих слов в комментариях."""
    expected_count = Comment.objects.count()
    bad_words_data = {'text': f'Какой-то текст, {word}, еще текст'}
    assertFormError(
        author_client.post(URL.detail, data=bad_words_data),
        form='form',
        field='text',
        errors=WARNING
    ), (f'Проверьте, что при вводе слова "{word}" '
        f'возникает ошибка "{WARNING}".')
    comparison_count_comments_in_db(expected_count)


def test_author_can_edit_comment(
        author, author_client, comment, form_data, news
):
    """Тест на редактирование комментария автором."""
    expected_count = Comment.objects.count()
    assertRedirects(
        author_client.post(URL.edit, data=form_data),
        f'{URL.detail}#comments',
        msg_prefix=('Проверьте, что после редактирования комментария '
                    f'произошел редирект на страницу "{URL.detail}".'),
    )
    comment.refresh_from_db()
    assert comment.news == news, (
        'Проверьте, что новость связана с комментарием.'
    )
    assert comment.author == author, (
        'Проверьте, что автор комментария совпадает.'
    )
    assert comment.text == COMMENT_TEXT_NEW, (
        'Проверьте, что комментарии совпадают.'
    )
    comparison_count_comments_in_db(expected_count)


def test_author_can_delete_comment(author_client, comment):
    """Тест на удаление комментария автором."""
    expected_count = Comment.objects.count() - 1
    assertRedirects(
        author_client.delete(URL.delete),
        f'{URL.detail}#comments',
        msg_prefix=('Проверьте, что после удаления комментария '
                    f'произошел редирект на страницу "{URL.detail}".'),
    )
    comparison_count_comments_in_db(expected_count)


def test_user_cant_edit_comment_of_another_user(
    admin_client, author, comment, form_data, news
):
    """Тест на редактирование комментария другим пользователем."""
    expected_count = Comment.objects.count()
    comment.refresh_from_db()
    assert comment.news == news, (
        'Проверьте, что новость связана с комментарием.'
    )
    assert comment.author == author, (
        'Проверьте, что автор комментария совпадает.'
    )
    assert comment.text == COMMENT_TEXT, (
        'Проверьте, что комментарии совпадают.'
    )
    return_status_404(admin_client.post(URL.edit, data=form_data))
    comparison_count_comments_in_db(expected_count)


def test_user_cant_delete_comment_of_another_user(admin_client):
    """Тест на удаление комментария другим пользователем."""
    expected_count = Comment.objects.count()
    return_status_404(admin_client.delete(URL.delete))
    comparison_count_comments_in_db(expected_count)
