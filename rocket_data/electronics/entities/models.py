from django.db import models
from products.models import Product


class Entity(models.Model):
    type = models.ForeignKey(
        'EntityType',
        on_delete=models.SET('undefined'),
        related_name='entities'
    )
    name = models.CharField(max_length=50, unique=True, null=False)
    products = models.ManyToManyField(
        Product,
        blank=True,
        related_name='entities'
    )
    supplier = models.ForeignKey(
        "Entity",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='consumers'
    )
    debt = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    contact = models.OneToOneField(
        'Contact',
        on_delete=models.CASCADE,
        primary_key=True
    )

    class Meta:
        verbose_name_plural = "Entities"

    def __str__(self):
        return f'{self.name} type {self.type}'


class Contact(models.Model):
    email = models.EmailField(blank=False)
    address = models.OneToOneField(
        'Address',
        on_delete=models.CASCADE,
        primary_key=True
    )


class Address(models.Model):
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    building = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = "Addresses"


class EntityType(models.Model):
    name = models.CharField(max_length=20, unique=True)
    level = models.IntegerField(unique=True)

    def __str__(self):
        return f'{self.name} - level {self.level}'





