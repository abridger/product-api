from datetime import (datetime,
                      timezone)
from django.test import TestCase
import os
from products.models import Product
from products.tasks import (_get_by_path,
                            _map_data_from_source,
                            import_products)


class GetByPathTestCase(TestCase):
    def test_the_correct_dictionary_key_is_returned_from_a_path(self):
        dict = {
            'primary': {
                'secondary': {
                    'tertiary': 'correct'
                }
            }
        }
        path = ['primary', 'secondary', 'tertiary']
        _get_by_path(dict, path)
        self.assertEqual(
            _get_by_path(dict, path),
            'correct'
        )

    def test_the_correct_dictionary_key_is_returned_from_a_path_with_index(self):
        dict = {
            'primary': {
                'secondary': {
                    'tertiary': [
                        'incorrect',
                        'correct'
                    ]
                }
            }
        }
        path = ['primary', 'secondary', 'tertiary', 1]
        _get_by_path(dict, path)
        self.assertEqual(
            _get_by_path(dict, path),
            'correct'
        )


class MapDataFromSourceTestCase(TestCase):
    def test_the_correct_data_is_returned(self):
        source = {
            'id': 'ID value',
            'primary': {
                'secondary': {
                    'tertiary': 'Tertiary value'
                }
            }
        }
        mappings = {
            'id': ['id'],
            'tertiary': ['primary', 'secondary', 'tertiary']
        }
        mapped_data = _map_data_from_source(mappings, source)
        self.assertEqual(
            mapped_data['id'],
            source['id']
        )
        self.assertEqual(
            mapped_data['tertiary'],
            source['primary']['secondary']['tertiary']
        )


class ImportProductsTestCase(TestCase):
    def test_that_a_value_error_is_raised_from_an_incorrect_directory(self):
        test_fixtures_directory = os.path.join(
            os.path.dirname(__file__),
            'invalid'
        )
        with self.assertRaises(ValueError):
            import_products(test_fixtures_directory)

    def test_that_products_are_correcty_imported(self):
        test_fixtures_directory = os.path.join(
            os.path.dirname(__file__),
            'fixtures'
        )
        import_products(test_fixtures_directory)
        self.assertEqual(
            Product.objects.count(),
            1
        )
        created_product = Product.objects.get()
        self.assertEqual(
            created_product.gtin,
            '123459876'
        )
        self.assertEqual(
            created_product.brand,
            'Test brand'
        )
        self.assertEqual(
            created_product.category_1,
            'Groceries'
        )
        self.assertEqual(
            created_product.category_2,
            'Fruit and Vegetables'
        )
        self.assertEqual(
            created_product.category_3,
            'Exotic'
        )
        self.assertEqual(
            created_product.description,
            'Test product description'
        )
        self.assertEqual(
            created_product.energy_100g,
            100
        )
        self.assertEqual(
            created_product.energy_serving,
            25
        )
        self.assertEqual(
            created_product.title,
            'Test product'
        )
        self.assertEqual(
            created_product.updated_at,
            datetime(2017, 7, 6, 15, 3, 19, tzinfo=timezone.utc)
        )
