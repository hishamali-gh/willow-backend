from rest_framework import serializers
from .models import ProductType, ProductImage, Product, ProductVariant

class ProductTypeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['id', 'name']

class ProductImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'url', 'main']
        read_only_fields = ['product']

class ProductModelSerializer(serializers.ModelSerializer):
    product_type = serializers.CharField(source='product_type.name')
    main_image = serializers.SerializerMethodField()
    image = serializers.URLField(write_only=True, required=False)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'category',
            'product_type',
            'description',
            'price',
            'main_image',
            'image',
            'is_active',
            'created_at',
            'updated_at'
        ]

    def get_main_image(self, obj):
        main = obj.images.filter(main=True).first()
        return main.url if main else None
    
    def create(self, validated_data):
        image_url = validated_data.pop('image', None)
        type_name = validated_data.pop('product_type')['name']

        product_type, _ = ProductType.objects.get_or_create(name=type_name)

        product = Product.objects.create(
            product_type=product_type,
            **validated_data
        )

        if image_url:
            ProductImage.objects.create(
                product=product,
                url=image_url,
                main=True
            )

        return product
    
    def update(self, instance, validated_data):
        image_url = validated_data.pop('image', None)

        if 'product_type' in validated_data:
            type_name = validated_data.pop('product_type')['name']
            product_type, _ = ProductType.objects.get_or_create(name=type_name)
            instance.product_type = product_type

        instance = super().update(instance, validated_data)

        if image_url:
            ProductImage.objects.update_or_create(
                product=instance,
                main=True,
                defaults={'url': image_url}
            )

        return instance

class ProductVariantModelSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )

    product = ProductModelSerializer(read_only=True)

    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'product_id', 'size', 'stock']
