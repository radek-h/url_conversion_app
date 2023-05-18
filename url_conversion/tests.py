from unittest.mock import patch

from django.urls import reverse
from rest_framework.test import APITestCase

from .models import URL as URLModel


class ConvertURLViewTest(APITestCase):
    def __init__(self, *args, **kwargs):
        super(ConvertURLViewTest, self).__init__(*args, **kwargs)
        self.url = reverse("convert-url")

    def test_get_convert_url_return_200_when_db_obj_exist_for_matching_full_url(self):
        url_obj = URLModel.objects.create(
            full_url="http://www.wp.pl", full_shorten_url="http://localhost:8000/abcde"
        )
        url_obj.save()

        response = self.client.get(self.url, {"url": "http://www.wp.pl"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, url_obj.full_shorten_url)

    def test_get_convert_url_return_200_when_db_obj_exist_for_matching_full_shorten_url(
        self,
    ):
        url_obj = URLModel.objects.create(
            full_url="http://www.wp.pl", full_shorten_url="http://localhost:8000/abcde"
        )
        url_obj.save()

        response = self.client.get(self.url, {"url": "http://localhost:8000/abcde"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, url_obj.full_url)

    def test_get_convert_url_return_404_when_db_obj_not_exist_and_passed_shorten_url(
        self,
    ):
        response = self.client.get(self.url, {"url": "http://localhost:8000/abcde"})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data["error"], "This shorten URL is not in our database."
        )

    def test_get_convert_url_return_400_when_empty_data_url(self):
        response = self.client.get(self.url, {"url": ""})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "URL cannot be blank nor none")

    @patch("url_conversion.views.generate_url_key")
    def test_get_convert_url_return_200_when_db_obj_not_exist_and_passed_full_url(
        self, mock_generate_url_key
    ):
        mock_generate_url_key.return_value = "12abc"
        response = self.client.get(self.url, {"url": "http://www.wp.pl"})
        url_obj = URLModel.objects.get(full_shorten_url="http://localhost:8000/12abc")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, url_obj.full_shorten_url)
