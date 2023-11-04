from http import HTTPStatus

from notes.tests.core import CoreTestCase, URL


class TestRoutes(CoreTestCase):

    def test_pages_availability(self):
        """Тест доступности страниц для всех."""
        urls = (
            (URL.home, self.client, HTTPStatus.OK),
        )
        for url, client, expected_status in urls:
            with self.subTest(url=url):
                self.assertEqual(
                    client.get(url).status_code, expected_status,
                    msg=('Код ответа не соответствует ожидаемому.')
                )
