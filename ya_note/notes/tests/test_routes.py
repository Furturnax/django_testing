from http import HTTPStatus

from notes.tests.core import CoreTestCase, URL


class TestRoutes(CoreTestCase):
    """Тест ulrs, сформированных в urls.py."""

    def test_pages_availability(self):
        """Тест доступа к страницам для любого пользователя."""
        urls = (
            (URL.home, self.client, HTTPStatus.OK),
            (URL.login, self.client, HTTPStatus.OK),
            (URL.logout, self.client, HTTPStatus.OK),
            (URL.signup, self.client, HTTPStatus.OK),
            (URL.add, self.user_client, HTTPStatus.OK),
            (URL.success, self.user_client, HTTPStatus.OK),
            (URL.list, self.user_client, HTTPStatus.OK),
            (URL.detail, self.author_client, HTTPStatus.OK),
            (URL.edit, self.author_client, HTTPStatus.OK),
            (URL.delete, self.author_client, HTTPStatus.OK),
            (URL.detail, self.user_client, HTTPStatus.NOT_FOUND),
            (URL.edit, self.user_client, HTTPStatus.NOT_FOUND),
            (URL.delete, self.user_client, HTTPStatus.NOT_FOUND),
        )
        for url, client, expected_status in urls:
            with self.subTest(url=url):
                self.assertEqual(
                    client.get(url).status_code,
                    expected_status,
                    msg=(f'Код ответа страницы {url} не'
                         'соответствует ожидаемому.'),
                )

    def test_redirect_for_anonymous_client(self):
        """Тест редиректа у анонимного пользователя."""
        urls = (
            (URL.list, self.client),
            (URL.success, self.client),
            (URL.add, self.client),
            (URL.detail, self.client),
            (URL.edit, self.client),
            (URL.delete, self.client),
        )
        for url, client in urls:
            with self.subTest(url=url):
                redirect_url = f'{URL.login}?next={url}'
                self.assertRedirects(
                    client.get(url),
                    redirect_url,
                    msg_prefix=('Проверьте, что неавторизованный пользователь'
                                f'не имеет доступа к странице {url}.')
                )
