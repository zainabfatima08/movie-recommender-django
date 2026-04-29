from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg, Count
from django.utils import timezone


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Genre(TimestampedModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class Person(TimestampedModel):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Movie(TimestampedModel):
    title = models.CharField(max_length=255)
    overview = models.TextField(blank=True)
    release_date = models.DateField(null=True, blank=True)
    tmdb_id = models.PositiveIntegerField(unique=True, null=True, blank=True)

    genres = models.ManyToManyField(Genre, related_name='movies', blank=True)
    cast = models.ManyToManyField(Person, related_name='movies', blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self) -> str:
        return self.title

    @property
    def average_rating(self) -> float:
        return self.reviews.aggregate(avg=Avg('rating')).get('avg') or 0

    @property
    def rating_count(self) -> int:
        return self.reviews.aggregate(total=Count('id')).get('total') or 0







