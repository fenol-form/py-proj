from django.db import models
from django.contrib.auth.models import User

from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator

class TVShowRate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    rating = models.CharField(max_length=10)
    years = models.CharField(max_length=10)
    countries = models.CharField(max_length=50)
    genres = models.CharField(max_length=50)
    description = models.CharField(max_length=2500)
    isInList = models.BooleanField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True, validators=(
        MinValueValidator(1),
        MaxValueValidator(10)
    ))