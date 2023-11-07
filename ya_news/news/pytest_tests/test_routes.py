from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

pytestmark = pytest.mark.django_db


def test_pages_availability_for_all(urls, client, pages_for_anonymous):
    """Тест доступа к страницам для любого пользователя."""
    for url in pages_for_anonymous:
        assert client.get(url).status_code == HTTPStatus.OK, (
            f'Проверьте, что код ответа {HTTPStatus.OK} страницы '
            f'"{urls.url}" соответствует ожидаемому.'
        )


def test_pages_availability_for_author_and_user(
        admin_client, author_client, comment, pages_for_author, urls
):
    """Тест доступа к страницам редактирования и удаления чужих коментариев."""
    for url in pages_for_author:
        assert author_client.get(url).status_code == HTTPStatus.OK, (
            f'Проверьте, что код ответа {HTTPStatus.OK} страницы '
            f'"{urls.url}" соответствует ожидаемому.'
        )
        assert admin_client.get(url).status_code == HTTPStatus.NOT_FOUND, (
            f'Проверьте, что код ответа {HTTPStatus.NOT_FOUND} страницы '
            f'"{urls.url}" соответствует ожидаемому.'
        )


def test_redirect_for_anonymous_client(
        client, urls, comment, pages_for_author
):
    """Тест редиректа у анонимного пользователя."""
    for url in pages_for_author:
        assertRedirects(
            client.get(url),
            f'{urls.login}?next={url}',
            msg_prefix=('Проверьте, что неавторизованный пользователь '
                        f'не имеет доступа к странице "{url}".'),
        )
