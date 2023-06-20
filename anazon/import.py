# scrapper to load data onto database
import django
import os
import requests


# avoid django.core.exceptions.ImproperlyConfigured
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anazon.settings')
django.setup()


def generate_category(categories):
    from shop.models import Category
    for category in categories:
        Category.objects.get_or_create(name=category)


def generate_product(products):
    from shop.models import Category, Product
    for product in products:
        Product.objects.get_or_create(
            title=product['title'], price=product['price'], description=product['description'], category=Category.objects.get(name=product['category']), image=product['thumbnail'])


if __name__ == "__main__":
    r = requests.get('https://dummyjson.com/products/categories')
    categories = r.json()
    generate_category(categories)

    r = requests.get('https://dummyjson.com/products?limit=100')
    products = r.json()['products']
    generate_product(products)
