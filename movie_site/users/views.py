from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from movies.models import Movie

from .forms import ReviewForm, WatchStatusForm
from .models import Review, UserMovieStatus
from .services import recommend_movies_for_user


class DashboardView(LoginRequiredMixin, View):
    template_name = 'users/dashboard.html'

    def get(self, request):
        statuses  = UserMovieStatus.objects.filter(user=request.user).select_related('movie')
        watchlist = statuses.filter(status=UserMovieStatus.Status.WATCHLIST)
        watched   = statuses.filter(status=UserMovieStatus.Status.WATCHED)

        context   = {
            'watchlist': watchlist,
            'watched': watched,
            'recommendations': recommend_movies_for_user(request.user, limit=8),
        }

        return render(request, self.template_name, context)


class ReviewCreateUpdateView(LoginRequiredMixin, View):
    def get(self, request, movie_id):
        movie  = get_object_or_404(Movie, id=movie_id)
        review = Review.objects.filter(user=request.user, movie=movie).first()
        form   = ReviewForm(instance=review)

        return render(request, 'users/review_form.html', {'form': form, 'movie': movie})

    def post(self, request, movie_id):
        movie  = get_object_or_404(Movie, id=movie_id)
        review = Review.objects.filter(user=request.user, movie=movie).first()
        form   = ReviewForm(request.POST, instance=review)

        if form.is_valid():
            payload       = form.save(commit=False)
            payload.user  = request.user
            payload.movie = movie
            payload.save()
            messages.success(request, 'Review saved successfully.')

            return redirect('movie-detail', movie_id=movie.id)
        return render(request, 'users/review_form.html', {'form': form, 'movie': movie})


class WatchStatusUpdateView(LoginRequiredMixin, View):
    def post(self, request, movie_id):
        movie      = get_object_or_404(Movie, id=movie_id)
        status_obj = UserMovieStatus.objects.filter(user=request.user, movie=movie).first()
        form       = WatchStatusForm(request.POST, instance=status_obj)

        if form.is_valid():
            payload       = form.save(commit=False)
            payload.user  = request.user
            payload.movie = movie
            payload.save()
            messages.success(request, 'Watch state updated.')
            
        else:
            messages.error(request, 'Could not update watch state.')
        return redirect('movie-detail', movie_id=movie.id)
