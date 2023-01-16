from datetime import datetime, timedelta

from celery import shared_task
import time

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Category


# @shared_task
# def hello():
#     time.sleep(10)
#     print('Hello, World!')


# @shared_task
# def printer(N):
#     for i in range(N):
#         time.sleep(1)
#         print(i + 1)


# @shared_task
# def mail_new():
#     post = Post.save(commit=False)
#     html_content = render_to_string(
#         'post_created_email.html',
#         {
#             'post': post,
#             'text': post.preview,
#             'link': f'http://127.0.0.1:8000/news/{post.pk}',
#         }
#     )
#
#     msg = EmailMultiAlternatives(
#         subject=f'{post.title}',
#         body=post.text,
#         from_email='andrey.bakiev75@yandex.ru',
#         to=Category.subscribers
#     )
#     msg.attach_alternative(html_content, "text/html")
#
#     msg.send()


@shared_task
def my_job():                                               # Еженедельная рассылка по расписанию из файла сelery.py
    today = datetime.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(date_time_post__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))


    html_content = render_to_string(
        'weekly_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts
        }

    )

    msg = EmailMultiAlternatives(
        subject = 'Статьи за неделю',
        body = '',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
