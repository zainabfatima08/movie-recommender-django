from __future__ import annotations

from collections import defaultdict

from django.contrib.auth import get_user_model

from movies.models import Movie

from .models import Review

User = get_user_model()


def recommend_movies_for_user(user, limit: int = 6):
    """Simple user-based collaborative filtering using overlapping ratings."""
    if not user.is_authenticated:
        return Movie.objects.none()

    my_ratings = dict(Review.objects.filter(user=user).values_list('movie_id', 'rating'))
    if not my_ratings:
        return Movie.objects.none()

    candidate_scores = defaultdict(float)

    for other in User.objects.exclude(id=user.id):
        other_ratings = dict(Review.objects.filter(user=other).values_list('movie_id', 'rating'))
        overlap = set(my_ratings).intersection(other_ratings)
        if not overlap:
            continue

        similarity = sum(5 - abs(my_ratings[m] - other_ratings[m]) for m in overlap) / (len(overlap) * 5)
        if similarity <= 0:
            continue

        for movie_id, rating in other_ratings.items():
            if movie_id in my_ratings:
                continue
            candidate_scores[movie_id] += rating * similarity

    sorted_ids = [movie_id for movie_id, _ in sorted(candidate_scores.items(), key=lambda x: x[1], reverse=True)]
    if not sorted_ids:
        return Movie.objects.none()

    movies_by_id = {m.id: m for m in Movie.objects.filter(id__in=sorted_ids).prefetch_related('genres')}
    ranked = [movies_by_id[movie_id] for movie_id in sorted_ids if movie_id in movies_by_id]
    return ranked[:limit]