from django.urls import reverse
from products.models import Product
from rest_framework import status
from rest_framework.test import APITestCase


class ProductRequestTests(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(
            gtin='123459876',
            brand='Test Brand',
            description='A test product',
            category_1='Groceries',
            category_2='Fresh Fruit',
            category_3='Exotic',
            energy_100g=200,
            energy_serving=100,
        )

    def tearDown(self):
        Product.objects.all().delete()

    def test_that_a_list_of_products_is_returned(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            len(response.data),
            Product.objects.count()
        )
        self.assertEqual(
            response.data[0]['id'],
            str(self.product.id)
        )
        self.assertEqual(
            response.data[0]['brand'],
            self.product.brand
        )
        self.assertEqual(
            response.data[0]['description'],
            self.product.description
        )

    def test_that_an_individual_product_is_returned(self):
        url = reverse(
            'product-detail',
            args=[self.product.id]
        )
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['id'],
            str(self.product.id)
        )
        self.assertEqual(
            response.data['brand'],
            self.product.brand
        )
        self.assertEqual(
            response.data['description'],
            self.product.description
        )

    def test_that_it_is_possible_to_display_only_requested_fields(self):
        url = reverse('product-list')
        url = url + '?fields=description'
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data[0]['description'],
            self.product.description
        )
        with self.assertRaises(KeyError):
            self.assertEqual(
                response.data[0]['brand'],
                self.product.brand
            )

    def test_that_categories_are_returned_as_a_list(self):
        url = reverse(
            'product-detail',
            args=[self.product.id]
        )
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['categories'],
            [
                self.product.category_1,
                self.product.category_2,
                self.product.category_3
            ]
        )

    def test_that_energy_information_is_returned_as_a_dictionary(self):
        url = reverse(
            'product-detail',
            args=[self.product.id]
        )
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['energy']['Per 100g'],
            self.product.energy_100g
        )
        self.assertEqual(
            response.data['energy']['Per Serving'],
            self.product.energy_serving
        )
