from http import HTTPStatus

from notes.tests.core import CoreTestCase, URL


class TestRoutes(CoreTestCase):

    def test_pages_availability(self):
        """Тест доступности страниц для всех."""
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
                    client.get(url).status_code, expected_status,
                    msg=('Код ответа не соответствует ожидаемому.')
                )
