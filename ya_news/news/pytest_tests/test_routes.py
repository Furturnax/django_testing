import pytest

from http import HTTPStatus
from pytest_django.asserts import assertRedirects

from conftest import ADMIN_USER, AUTHOR_USER, CLIENT_USER, URL

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url, parametrized_client, exp_status',
    (
        (URL.home, CLIENT_USER, HTTPStatus.OK),
        (URL.login, CLIENT_USER, HTTPStatus.OK),
        (URL.logout, CLIENT_USER, HTTPStatus.OK),
        (URL.signup, CLIENT_USER, HTTPStatus.OK),
        (URL.edit, AUTHOR_USER, HTTPStatus.OK),
        (URL.delete, AUTHOR_USER, HTTPStatus.OK),
        (URL.edit, ADMIN_USER, HTTPStatus.NOT_FOUND),
        (URL.delete, ADMIN_USER, HTTPStatus.NOT_FOUND),
    )
)
def test_pages_availability(
    url, parametrized_client, exp_status, comment
):
    """Тест доступа к страницам для любого пользователя."""
    assert parametrized_client.get(url).status_code == exp_status, (
        f'Проверьте, код ответа страницы {url} не соответствует ожидаемому.'
    )


@pytest.mark.parametrize(
    'url, parametrized_client',
    (
        (URL.edit, CLIENT_USER),
        (URL.delete, CLIENT_USER),
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
                    f'не имеет доступа к странице {url}.'),
    )
