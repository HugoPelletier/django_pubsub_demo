import time
import uuid
from enum import Enum
from typing import Dict

import requests
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class ColorChoice(Enum):  # A subclass of Enum
    BLACK = "Black"
    RED = "Red"
    GREEN = "Green"
    BLUE = "Blue"
    YELLOW = "Yellow"


class SizeChoice(Enum):  # A subclass of Enum
    XXS = "XX-Small"
    S = "Small"
    M = "Medium"
    L = "Large"
    XXL = "XX-Large"


class Category(models.Model):
    name = models.CharField(max_length=100)
    activate = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)
    activate = models.BooleanField(default=True)
    search = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=400)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    sold_out = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Skus(models.Model):
    sku = models.CharField(max_length=20)
    color = models.CharField(
        max_length=10,
        choices=[(tag.name, tag.value) for tag in ColorChoice]
    )
    size = models.CharField(
        max_length=5,
        choices=[(tag.name, tag.value) for tag in SizeChoice]
    )
    price_min = models.IntegerField()
    price_max = models.IntegerField()
    inventory = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.sku


@receiver(post_save, sender=Product)
def product_post_save(sender, instance, **kwargs):
    print('product')
    print(instance.name)
    build_product_aggregate(instance.id)


@receiver(post_save, sender=Skus)
def sku_post_save(sender, instance, **kwargs):
    print('sku')
    print(instance.sku)
    build_product_aggregate(instance.product.id)


@receiver(post_save, sender=Brand)
def brand_post_save(sender, instance, **kwargs):
    print('brand')
    print(instance.name)

    # build brand aggregate
    aggregate = {
        'metadata': {
            'topic': 'Products.Brand',
            'version': '1.0.0',
            'publication': int(time.time() * 1000)
        },
        'aggregate': {
            'state': 'active',
            'version': int(time.time() * 1000),
            'id': instance.id,
            'name': instance.name,
            'available_to_search': instance.search
        }
    }

    product_post_save()
    print(send_to_pubsub(aggregate))


def build_product_aggregate(product_id):
    print('build product aggregate')
    print(product_id)


def send_to_pubsub(aggregate: Dict) -> Dict:
    """
    Send request to the pubsub service

    :param aggregate: dict
    :return: dict
    """

    response = requests.post('http://demo-pubsub:8080/messages',
                             json=aggregate,
                             headers={'x-request-id': str(uuid.uuid4())})
    print(response)
