# scrapper to load data onto database
import django
import os
import requests


# avoid django.core.exceptions.ImproperlyConfigured
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anazon.settings')
django.setup()


def generate_category(category):
    from shop.models import Category
    for c in category:
        Category.objects.get_or_create(name=c)


def generate_product(product):
    from shop.models import Category, Product
    for p in product:
        Product.objects.get_or_create(
            title=p['title'], price=p['price'], description=p['description'], category=Category.objects.get(name=p['category']), image=p['image'])


if __name__ == "__main__":
    r = requests.get('https://fakestoreapi.com/products')
    data = r.json()
    category = set([d['category'] for d in data])
    generate_category(category)
    generate_product(data)
