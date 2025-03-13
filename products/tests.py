from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from products.models import Product, ProductPhoto

class ProductListAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('product-list')

        # Создадим пару продуктов
        self.product1 = Product.objects.create(name='Test Product 1')
        self.product2 = Product.objects.create(name='Test Product 2')

        # Фото для product1
        ProductPhoto.objects.create(
            product=self.product1,
            image_url='http://example.com/photo1_global.jpg',
            city_id=None
        )
        ProductPhoto.objects.create(
            product=self.product1,
            image_url='http://example.com/photo1_city10.jpg',
            city_id=10
        )


        ProductPhoto.objects.create(
            product=self.product2,
            image_url='http://example.com/photo2_global.jpg',
            city_id=None
        )

    def test_get_products_without_city_header(self):

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(len(data), 2)


        product1_photos = data[0]['photos']
        self.assertEqual(len(product1_photos), 1)
        self.assertEqual(product1_photos[0]['image_url'], 'http://example.com/photo1_global.jpg')


        product2_photos = data[1]['photos']
        self.assertEqual(len(product2_photos), 1)
        self.assertEqual(product2_photos[0]['image_url'], 'http://example.com/photo2_global.jpg')

    def test_get_products_with_city_header_10(self):

        response = self.client.get(self.url, HTTP_X_CITY_ID='10')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        product1_photos = data[0]['photos']
        self.assertEqual(len(product1_photos), 1)
        self.assertEqual(product1_photos[0]['image_url'], 'http://example.com/photo1_city10.jpg')


        product2_photos = data[1]['photos']
        self.assertEqual(len(product2_photos), 1)
        self.assertEqual(product2_photos[0]['image_url'], 'http://example.com/photo2_global.jpg')

    def test_get_products_with_incorrect_city_header(self):

        response = self.client.get(self.url, HTTP_X_CITY_ID='abc')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        product1_photos = data[0]['photos']
        self.assertEqual(len(product1_photos), 1)
        self.assertEqual(product1_photos[0]['image_url'], 'http://example.com/photo1_global.jpg')


        product2_photos = data[1]['photos']
        self.assertEqual(len(product2_photos), 1)
        self.assertEqual(product2_photos[0]['image_url'], 'http://example.com/photo2_global.jpg')
