from datetime import datetime
from functools import reduce
from products.models import Product
from products.serializers import ProductSerializer
import operator
from os import (listdir,
                path)
import xmltodict

# These mappings are only very provisional, since they rely on positional
# references - eg, with the `gtin` and `energy`. These are consistent in
# the products provided, but may not be in future products information.
# It would be better to look these up based on the tag name. This also does
# not allow for more complex mappings, eg. adding the code to product
# categories (`01 - Fruit & Vegetables`)
PRODUCT_KEY_MAPPINGS = {
    'gtin': [
        'Product',
        'Identity',
        'ProductCodes',
        'Code',
        0,
        '#text'
    ],
    'brand': [
        'Product',
        'Identity',
        'Subscription',
        '#text'
    ],
    'description': [
        'Product',
        'Data',
        'Language',
        'Description'
    ],
    'category_1': [
        'Product',
        'Data',
        'Language',
        'Categorisations',
        'Categorisation',
        'Level',
        0,
        '#text'
    ],
    'category_2': [
        'Product',
        'Data',
        'Language',
        'Categorisations',
        'Categorisation',
        'Level',
        1,
        '#text'
    ],
    'category_3': [
        'Product',
        'Data',
        'Language',
        'Categorisations',
        'Categorisation',
        'Level',
        2,
        '#text'
    ],
    'energy_100g': [
        'Product',
        'Data',
        'Language',
        'ItemTypeGroup',
        'NumericNutrition',
        'NutrientValues',
        1,
        'Per100',
        'Value'
    ],
    'energy_serving': [
        'Product',
        'Data',
        'Language',
        'ItemTypeGroup',
        'NumericNutrition',
        'NutrientValues',
        1,
        'PerServing',
        'Value'
    ],
    'title': [
        'Product',
        'Identity',
        'DiagnosticDescription',
        '#text'
    ],
    'updated_at': [
        'Product',
        '@VersionDateTime'
    ]
}


def _get_by_path(root, items):
    """Access a nested object in root by item sequence."""
    return reduce(operator.getitem, items, root)


def _map_data_from_source(mappings, source):
    """
    Extract the data from the source dictionary using the mappings provided.
    """
    results = {}
    for item in mappings:
        try:
            results[item] = _get_by_path(source, mappings[item])
        except KeyError:
            pass
    return results


def import_products(directory):
    """
    Read a directory of XML files, build a dictionary for each product and
    create a product from each dictionary of product details.
    """
    try:
        fixtures = listdir(directory)
    except FileNotFoundError:
        raise ValueError('Directory not found')
    for fixture in fixtures:
        file = open(
            path.join(
                directory,
                fixture
            )
        )
        file_data = file.read()
        file.close()
        # Parse the XML in the file and convert it to a Python dictionary.
        product_data = xmltodict.parse(file_data)
        # Convert the product data into a flat dictionary that matches the
        # structure of the Product model.
        mapped_data = _map_data_from_source(
            PRODUCT_KEY_MAPPINGS,
            product_data
        )
        # Convert the `updated_at` string to a datetime object. Again, this is
        # a slight shortcoming of using the mappings object, which could be
        # replaced with a more sophisticated function in future.
        mapped_data['updated_at'] = datetime.strptime(
            mapped_data['updated_at'],
            '%Y-%m-%dT%H:%M:%S%z'
        )
        # Create the product if necessary, or retrieve it based on the `gtin`
        # field, so that we can update it with the latest data.
        product, created = Product.objects.get_or_create(
            gtin=mapped_data['gtin']
        )
        # Use the serializer to update our product with the complete set of
        # data and save.
        product_serializer = ProductSerializer(
            instance=product,
            data=mapped_data
        )
        if product_serializer.is_valid():
            product_serializer.save()
        else:
            raise Exception(serializer.errors)
