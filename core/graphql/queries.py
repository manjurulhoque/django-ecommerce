import graphene
from graphene_django import DjangoObjectType

from core.graphql.core_graphql.exceptions import GraphQLError
from core.models import Product, Category


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = "__all__"


class ProductQuery(graphene.ObjectType):
    products = graphene.List(ProductType)
    product = graphene.Field(ProductType, id=graphene.ID(required=True))

    def resolve_products(root, info):
        return Product.objects.all()

    def resolve_product(root, info, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            raise GraphQLError(f"Product with the id: {id} doesn't exist")


class CategoryQuery(graphene.ObjectType):
    categories = graphene.List(CategoryType)
    category = graphene.Field(CategoryType, id=graphene.ID(required=True))

    def resolve_categories(root, info):
        return Category.objects.all()

    def resolve_category(root, info, id):
        try:
            return Category.objects.get(id=id)
        except Category.DoesNotExist:
            raise GraphQLError(f"Category with the id: {id} doesn't exist")
