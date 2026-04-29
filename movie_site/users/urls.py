from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import DashboardView, ReviewCreateUpdateView, WatchStatusUpdateView

urlpatterns = [
    path('dashboard/',                    DashboardView.as_view(),          name='dashboard'),
    path('movies/<int:movie_id>/review/', ReviewCreateUpdateView.as_view(), name='movie-review'),
    path('movies/<int:movie_id>/status/', WatchStatusUpdateView.as_view(),  name='movie-status'),

    path('accounts/login/',               LoginView.as_view(template_name='users/login.html'), name='login'),
    path('accounts/logout/',              LogoutView.as_view(next_page='movie-list'), name='logout'),
]