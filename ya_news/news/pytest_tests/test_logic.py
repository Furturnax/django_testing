import pytest

from http import HTTPStatus
from pytest_django.asserts import assertFormError, assertRedirects

from conftest import URL, COMMENT_TEXT, NEW_COMMENT_TEXT
from news.forms import BAD_WORDS, WARNING
from news.models import Comment

pytestmark = pytest.mark.django_db


def test_anonymous_user_cant_create_comment(client, form_data, news):
    """Тест на создание комментария анонимным пользователем."""
    expected_count = Comment.objects.count()
    client.post(URL.detail, data=form_data)
    comments_count = Comment.objects.count()
    assert expected_count == comments_count, (
        'Проверьте, что анонимный пользователь не может '
        'писать комментарии.'
    )


def test_auth_user_can_create_comment(author, author_client, form_data, news):
    """Тест на создание комментария авторизированным пользователем."""
    expected_count = Comment.objects.count() + 1
    responce = author_client.post(URL.detail, data=form_data)
    comments_count = Comment.objects.count()
    assertRedirects(
        responce,
        f'{URL.detail}#comments',
        msg_prefix=('Проверьте, что произошел редирект на страницу '
                    f'"{URL.detail}".'),
    )
    assert expected_count == comments_count, (
        'Проверьте, что авторизированный пользователь смог написать '
        'комментарий.'
    )
    new_comment = Comment.objects.get()
    assert all(
        (
            new_comment.news == news,
            new_comment.author == author,
            new_comment.text == form_data['text'],
        )
    ), ('Проверьте, что написанный комментрарий имеет связанную с собой '
        'новость, указан автор комментария, написан текст комментария.')


@pytest.mark.parametrize(
    'word',
    (BAD_WORDS),
)
def test_user_cant_use_bad_words_in_comments(author_client, news, word):
    """Тест на запрет написания плохих слов в комментариях."""
    bad_words_data = {'text': f'Какой-то текст, {word}, еще текст'}
    expected_count = Comment.objects.count()
    responce = author_client.post(URL.detail, data=bad_words_data)
    comments_count = Comment.objects.count()
    assertFormError(
        responce,
        form='form',
        field='text',
        errors=WARNING
    ), (f'Проверьте, что при вводе слова "{word}" '
        f'возникает ошибка "{WARNING}".')
    assert expected_count == comments_count, (
        'Проверьте, что комментарий с запрещенным словом '
        'не отображается в списке комментариев.'
    )


def test_author_can_edit_comment(
        author, author_client, comment, form_data
):
    """Тест на редактирование комментария автором."""
    expected_count = Comment.objects.count()
    responce = author_client.post(URL.edit, data=form_data)
    assertRedirects(
        responce,
        f'{URL.detail}#comments',
        msg_prefix=('Проверьте, что после редактирования комментария '
                    f'произошел редирект на страницу "{URL.detail}".'),
    )
    comment.refresh_from_db()
    comments_count = Comment.objects.count()
    assert expected_count == comments_count, (
        'Проверьте, что количество комментариев, после редактирования, '
        'в общем списке не изменилось.'
    )
    assert all(
        (
            comment.text == NEW_COMMENT_TEXT,
            comment.author == author,
        )
    ), ('Проверьте, что после редактирования комментария он '
        'отображается в общем списке комментариев.')


def test_author_can_delete_comment(author_client, comment):
    """Тест на удаление комментария автором."""
    expected_count = Comment.objects.count() - 1
    response = author_client.delete(URL.delete)
    comments_count = Comment.objects.count()
    assertRedirects(
        response,
        f'{URL.detail}#comments',
        msg_prefix=('Проверьте, что после удаления комментария '
                    f'произошел редирект на страницу "{URL.detail}".'),
    )
    assert expected_count == comments_count, (
        'Проверьте, что количество комментариев, после удаления, '
        'в общем списке изменилось.'
    )


def test_user_cant_edit_comment_of_another_user(
    admin_client, author, comment, form_data
):
    """Тест на редактирование комментария другим пользователем."""
    expected_count = Comment.objects.count()
    response = admin_client.post(URL.edit, data=form_data)
    comment.refresh_from_db()
    comments_count = Comment.objects.count()
    assert response.status_code == HTTPStatus.NOT_FOUND, (
        'Проверьте, что при редактировании комментария не автором '
        'выводится ошибка 404.'
    )
    assert expected_count == comments_count, (
        'Проверьте, что количество комментариев, после попытки '
        'редактирования, в общем списке не изменилось.'
    )
    assert all(
        (
            comment.text == COMMENT_TEXT,
            comment.author == author
        )
    ), ('Проверьте, что при попытке редактирования комментария не автором '
        'комментарий не изменился.')


def test_user_cant_delete_comment_of_another_user(admin_client, comment):
    """Тест на удаление комментария другим пользователем."""
    expected_count = Comment.objects.count()
    response = admin_client.delete(URL.delete)
    comments_count = Comment.objects.count()
    assert response.status_code == HTTPStatus.NOT_FOUND, (
        'Проверьте, что при удалении комментария не автором '
        'выводится ошибка 404.'
    )
    assert expected_count == comments_count, (
        'Проверьте, что количество комментариев, после попытки удаления, '
        'в общем списке не изменилось.'
    )
