from rest_framework import serializers

from core.models import Product, Category


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        excluded_fields = kwargs.pop('excluded_fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields and excluded_fields:
            raise serializers.ValidationError("You can't pass fields and excluded fields together")

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if excluded_fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(excluded_fields)
            existing = set(self.fields.keys())
            for field_name in excluded_fields:
                self.fields.pop(field_name)


class CategorySerializer(DynamicFieldsModelSerializer):
    total_products = serializers.SerializerMethodField(method_name='total_products_count')

    class Meta:
        model = Category
        exclude = ("is_active",)

    def total_products_count(self, obj):
        return obj.product_set.count()

    # def to_representation(self, instance):
    #     identifiers = dict()
    #     identifiers['email'] = instance.Email
    #     identifiers['phone'] = instance.phone
    #
    #     representation = {
    #         'identifiers': identifiers,
    #         'activity_type': instance.xxxx,
    #         'timestamp': instance.xxxxx,
    #     }
    #
    #     return representation


class ProductSerializer(DynamicFieldsModelSerializer):
    category = CategorySerializer(fields=('id', 'title', 'slug', 'description', 'image'))

    class Meta:
        model = Product
        fields = "__all__"


class CategoryDetailsSerializer(DynamicFieldsModelSerializer):
    total_products = serializers.SerializerMethodField(method_name='total_products_count')
    product_set = ProductSerializer(many=True, excluded_fields=('category',))

    class Meta:
        model = Category
        exclude = ("is_active",)

    def total_products_count(self, obj):
        return obj.product_set.count()
