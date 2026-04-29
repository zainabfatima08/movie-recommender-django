from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

import requests

from movies.models import Genre, Movie, Person


class Command(BaseCommand):
    help = 'Seed movie catalog from TMDB trending API and credits endpoint.'

    def add_arguments(self, parser):
        parser.add_argument('--pages', type=int, default=1)

    def handle(self, *args, **options):
        api_key = settings.TMDB_API_KEY
        if not api_key:
            raise CommandError('TMDB_API_KEY is missing.')

        pages = options['pages']
        for page in range(1, pages + 1):
            self.stdout.write(self.style.NOTICE(f'Fetching page {page}...'))
            response = requests.get(
                'https://api.themoviedb.org/3/trending/movie/week',
                params={'api_key': api_key, 'page': page},
                timeout=20,
            )
            response.raise_for_status()

            payload = response.json()
            for item in payload.get('results', []):
                movie, _ = Movie.objects.get_or_create(
                    tmdb_id=item['id'],
                    defaults={
                        'title': item.get('title', 'Unknown'),
                        'overview': item.get('overview', ''),
                        'release_date': item.get('release_date') or None,
                    },
                )

                for genre_id in item.get('genre_ids', []):
                    genre, _ = Genre.objects.get_or_create(name=f'Genre {genre_id}')
                    movie.genres.add(genre)

                credits = requests.get(
                    f"https://api.themoviedb.org/3/movie/{item['id']}/credits",
                    params={'api_key': api_key},
                    timeout=20,
                )
                if credits.ok:
                    cast_data = credits.json().get('cast', [])[:5]
                    for cast_member in cast_data:
                        person, _ = Person.objects.get_or_create(name=cast_member['name'])
                        movie.cast.add(person)

                movie.save()

        self.stdout.write(self.style.SUCCESS('TMDB seed completed.'))