from django.db.models import Avg, Count

from .models import Movie


def top_movies(limit: int = 10):
    return (
        Movie.objects.annotate(avg_rating=Avg('reviews__rating'), votes=Count('reviews__id'))
        .filter(votes__gt=0)
        .order_by('-avg_rating', '-votes')[:limit]
    )