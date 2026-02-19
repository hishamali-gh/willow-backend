import json
from decimal import Decimal
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from products.models import Product, ProductType, ProductImage


class Command(BaseCommand):
    help = "Seed products into database"

    def handle(self, *args, **kwargs):

        # Clear existing (dev only)
        ProductImage.objects.all().delete()
        Product.objects.all().delete()
        ProductType.objects.all().delete()

        # Load JSON safely
        file_path = Path(settings.BASE_DIR) / "products" / "products.json"

        with open(file_path) as f:
            data = json.load(f)

        products_data = data["products"]

        # Create ProductTypes safely
        type_names = set(item["type"] for item in products_data)

        product_types = {}
        for name in type_names:
            obj, _ = ProductType.objects.get_or_create(name=name)
            product_types[name] = obj

        # Create Products
        product_objects = []

        for item in products_data:
            product_objects.append(
                Product(
                    name=item["name"],
                    category=item["category"].upper(),
                    product_type=product_types[item["type"]],
                    description=item["description"],
                    price=Decimal(item["price"]),
                    count=item["count"],
                )
            )

        created_products = Product.objects.bulk_create(product_objects, batch_size=100)

        # Create Images
        image_objects = []

        for product_obj, item in zip(created_products, products_data):
            for url in item["images"]:
                image_objects.append(
                    ProductImage(product=product_obj, url=url)
                )

        ProductImage.objects.bulk_create(image_objects, batch_size=100)

        self.stdout.write(self.style.SUCCESS("Products inserted successfully."))
