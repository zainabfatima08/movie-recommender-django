from django.contrib import admin

from .models import Genre, Movie, Person


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'tmdb_id')
    search_fields = ('title',)
    filter_horizontal = ('genres', 'cast')


admin.site.register(Genre)
admin.site.register(Person)
