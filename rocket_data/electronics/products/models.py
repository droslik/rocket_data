from django.db import models
from .validators import validate_date


class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    model = models.CharField(max_length=50)
    launch_date = models.DateField(blank=False, validators=[validate_date])


