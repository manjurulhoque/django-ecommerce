import graphene
from graphene_django import DjangoObjectType

from core.models import Product


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"


class ProductQuery(graphene.ObjectType):
    products = graphene.List(ProductType)

    def resolve_products(root, info):
        return Product.objects.all()
