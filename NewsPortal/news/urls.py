from django.urls import path
# Импортируем созданное нами представление
from .views import NewsList, NewDetail, SearchNewsList, NewsCreate, NewsUpdate, NewsDelete, ArticlesCreate, \
   ArticlesUpdate, ArticlesDelete

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем новостям у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('news/', NewsList.as_view(), name='news_list'),
   path('articles/', NewsList.as_view(), name='articles_list'),
 # pk — это первичный ключ новости, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('news/<int:pk>', NewDetail.as_view(), name='post_detail'),
   path('articles/<int:pk>', NewDetail.as_view(), name='articles_detail'),
   path('news/search/', SearchNewsList.as_view()),
   path('articles/search/', SearchNewsList.as_view()),

   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),

   path('articles/create/', ArticlesCreate.as_view(), name='atrticles_create'),
   path('articles/<int:pk>/edit/', ArticlesUpdate.as_view(), name='articles_edit'),
   path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'),

]
