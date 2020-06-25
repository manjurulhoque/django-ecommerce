from rest_framework.generics import ListAPIView, RetrieveAPIView

from .serializers import *
from .paginations import *


class ProductListAPIView(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductSetPagination
    queryset = Product.objects.select_related('category').filter(is_active=True).order_by('-id')


class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.select_related('category').filter(is_active=True)
    serializer_class = ProductSerializer
