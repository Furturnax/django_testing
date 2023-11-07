from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

from conftest import ANONYM, AUTH_USER, AUTHOR, URL

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url, parametrized_client, exp_status',
    (
        (URL.home, ANONYM, HTTPStatus.OK),
        (URL.login, ANONYM, HTTPStatus.OK),
        (URL.logout, ANONYM, HTTPStatus.OK),
        (URL.signup, ANONYM, HTTPStatus.OK),
        (URL.edit, AUTHOR, HTTPStatus.OK),
        (URL.delete, AUTHOR, HTTPStatus.OK),
        (URL.edit, AUTH_USER, HTTPStatus.NOT_FOUND),
        (URL.delete, AUTH_USER, HTTPStatus.NOT_FOUND),
    )
)
def test_pages_availability(
    url, parametrized_client, exp_status, comment
):
    """Тест доступа к страницам для любого пользователя."""
    assert parametrized_client.get(url).status_code == exp_status, (
        f'Проверьте, что код ответа страницы "{url}" соответствует ожидаемому.'
    )


@pytest.mark.parametrize(
    'url, parametrized_client',
    (
        (URL.edit, ANONYM),
        (URL.delete, ANONYM),
    )
)
def test_redirect_for_anonymous_client(
    url, parametrized_client
):
    """Тест редиректа у анонимного пользователя."""
    assertRedirects(
        parametrized_client.get(url),
        f'{URL.login}?next={url}',
        msg_prefix=('Проверьте, что неавторизованный пользователь '
                    f'не имеет доступа к странице "{url}".'),
    )
