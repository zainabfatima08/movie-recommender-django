from django.urls import path

from .views import MovieDetailView, MovieListView

urlpatterns = [
    path('',                       MovieListView.as_view(),   name='movie-list'),
    path('movies/<int:movie_id>/', MovieDetailView.as_view(), name='movie-detail'),
]