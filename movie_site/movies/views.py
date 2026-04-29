from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, render
from django.views import View

from users.models import Review, UserMovieStatus
from users.services import recommend_movies_for_user

from .models import Genre, Movie

#-------------LIST VIEW-------------------

class MovieListView(View):
    template_name = 'movies/movie_list.html'

    def get(self, request):
        query = request.GET.get('q', '').strip()
        genre_id = request.GET.get('genre')
        movies = Movie.objects.prefetch_related('genres').annotate(avg_rating=Avg('reviews__rating'),
                                                                   total_reviews=Count('reviews'))

        if query:
            for term in query.split():
                movies = movies.filter(
                    Q(title__icontains=term) | Q(overview__icontains=term) | Q(cast__name__icontains=term)
                )
            movies = movies.distinct()
        if genre_id:
            movies = movies.filter(genres__id=genre_id)

        context = {
            'movies'      : movies,
            'genres'      : Genre.objects.all(),
            'active_genre': int(genre_id) if genre_id and genre_id.isdigit() else None,
            'query'       : query,
        }
        return render(request, self.template_name, context)

#-----------DETAIL VIEW--------------------------

class MovieDetailView(View):
    template_name = 'movies/movie_detail.html'

    def get(self, request, movie_id):
        movie        = get_object_or_404(Movie.objects.prefetch_related('genres', 'cast', 'reviews__user'), id=movie_id)
        review       = None
        watch_status = None

        if request.user.is_authenticated:
            review       = Review.objects.filter(user=request.user, movie=movie).first()
            watch_status = UserMovieStatus.objects.filter(user=request.user, movie=movie).first()

        context = {
            'movie': movie,
            'review': review,
            'watch_status': watch_status,
            'recommendations': recommend_movies_for_user(request.user, limit=6),
            'reviews': movie.reviews.select_related('user').all(),
        }

        return render(request, self.template_name, context)
