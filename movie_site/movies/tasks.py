from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .services import top_movies


@shared_task

def send_weekly_top_movies_digest() -> int:
    User   = get_user_model()
    users  = User.objects.filter(is_active=True, email__isnull=False).exclude(email='')
    movies = top_movies(limit=10)

    sent = 0
    for user in users:
        body = render_to_string('movies/email/weekly_digest.txt', {'user': user, 'movies': movies})

        send_mail(
            subject       ='Weekly Top Movies Digest',
            message       =body,
            from_email    =None,
            recipient_list=[user.email],
            fail_silently =True,
        )
        sent += 1

    return sent