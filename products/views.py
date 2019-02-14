from products.models import Product
from products.serializers import ProductSerializer
from rest_framework import (mixins,
                            viewsets)


class ProductViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    filter_backends = ()
    permission_classes = ()
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
