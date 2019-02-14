from rest_framework import serializers
from products.models import Product


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        request = self.context.get('request', None)
        if request:
            fields = request.query_params.get('fields', None)
            if fields:
                fields = fields.split(',')
                # Drop any fields that are not specified
                # in the `fields` argument.
                allowed = set(fields)
                existing = set(self.fields.keys())
                for field_name in existing - allowed:
                    self.fields.pop(field_name)


class ProductSerializer(DynamicFieldsModelSerializer):
    """
    A ModelSerializer for the Product model.
    """
    categories = serializers.SerializerMethodField()
    energy = serializers.SerializerMethodField()

    def get_categories(self, product):
        return [
            product.category_1,
            product.category_2,
            product.category_3
        ]

    def get_energy(self, product):
        return {
            'Per 100g': product.energy_100g,
            'Per Serving': product.energy_serving
        }

    class Meta:
        model = Product
        fields = (
            'id',
            'gtin',
            'brand',
            'categories',
            'category_1',
            'category_2',
            'category_3',
            'description',
            'energy',
            'energy_100g',
            'energy_serving',
            'title',
            'updated_at'
        )
        extra_kwargs = {
            'category_1': {
                'write_only': True
            },
            'category_2': {
                'write_only': True
            },
            'category_3': {
                'write_only': True
            },
            'energy_100g': {
                'write_only': True
            },
            'energy_serving': {
                'write_only': True
            }
        }
