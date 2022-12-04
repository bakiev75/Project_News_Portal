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

   path('', NewsList.as_view(), name='articles_list'),
 # pk — это первичный ключ новости, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', NewDetail.as_view(), name='articles_detail'),
   path('search/', SearchNewsList.as_view()),
   path('create/', ArticlesCreate.as_view(), name='atrticles_create'),
   path('<int:pk>/edit/', ArticlesUpdate.as_view(), name='articles_edit'),
   path('<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'),

]