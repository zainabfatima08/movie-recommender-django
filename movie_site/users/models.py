from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        abstract = True

class UserMovieStatus(TimestampedModel):
    class Status(models.TextChoices):
        WATCHLIST = 'watchlist', 'Watchlist'
        WATCHED   = 'watched', 'Watched'

    user        = models.ForeignKey(User, on_delete = models.CASCADE)
    movie       = models.ForeignKey('movies.Movie', on_delete = models.CASCADE)
    status      = models.CharField(max_length = 20, choices = Status.choices)
    watched_on  = models.DateField(null = True, blank = True)

    class Meta:
        unique_together = ('user', 'movie')

    def save(self, *args, **kwargs):
        if self.status == self.status.WATCHED and self.watched_on is None:
            self.watched_on = timezone.localdate()
        super().save(*args, **kwargs)

class Review(TimestampedModel):
    user    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    movie   = models.ForeignKey('movies.Movie',       on_delete=models.CASCADE,  related_name='reviews')

    rating  = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)

    class Meta:
        unique_together = ('user', 'movie')
        ordering        = ['-created_at']





