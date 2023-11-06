import pytest

from pytest_django.asserts import assertFormError, assertRedirects

from conftest import (
    comparison_count_comments_in_db,
    return_status_404,
    COMMENT_TEXT,
    NEW_COMMENT_TEXT,
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


def test_auth_user_can_create_comment(author, author_client, form_data, news):
    """Тест на создание комментария авторизированным пользователем."""
    expected_count = Comment.objects.count() + 1
    assertRedirects(
        author_client.post(URL.detail, data=form_data),
        f'{URL.detail}#comments',
        msg_prefix=('Проверьте, что произошел редирект на страницу '
                    f'"{URL.detail}".'),
    )
    assert all(
        (Comment.objects.get().news == news,
         Comment.objects.get().author == author,
         Comment.objects.get().text == form_data['text'],)
    ), ('Проверьте, что написанный комментарий имеет связанную с собой '
        'новость, указан автор комментария, написан текст комментария.')
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
        author, author_client, comment, form_data
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
    assert all(
        (comment.text == NEW_COMMENT_TEXT,
         comment.author == author,)
    ), ('Проверьте, что после редактирования комментария он '
        'отображается в общем списке комментариев.')
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
    admin_client, author, comment, form_data
):
    """Тест на редактирование комментария другим пользователем."""
    expected_count = Comment.objects.count()
    comment.refresh_from_db()
    assert all(
        (comment.text == COMMENT_TEXT,
         comment.author == author)
    ), ('Проверьте, что при попытке редактирования комментария не автором '
        'комментарий не изменился.')
    return_status_404(admin_client.post(URL.edit, data=form_data))
    comparison_count_comments_in_db(expected_count)


def test_user_cant_delete_comment_of_another_user(admin_client):
    """Тест на удаление комментария другим пользователем."""
    expected_count = Comment.objects.count()
    return_status_404(admin_client.delete(URL.delete))
    comparison_count_comments_in_db(expected_count)
